from constants import Constants, Types
import helpers

# Stores variables for a block
# Includes name, type and if it is public in case of class
class VariableDirectory:
  # Initializes object with empty dictionary
  # Each value will be [Type, is_public, array_dimensions, memory_address]
  def __init__(self):
    self._variable_table = {}
  
  # Returns type and memory address of variable
  def get_variable_type(self, var_name):
    if self.variable_exists(var_name):
      return self._variable_table[var_name][0]
    return None

  # Returns is_public of variable
  def get_variable_is_public(self, var_name):
    if self.variable_exists(var_name):
      return self._variable_table[var_name][1]
    return None

  # Returns variable dimensions list
  def get_variable_dimensions(self, var_name):
    if self.variable_exists(var_name):
      return self._variable_table[var_name][2]
    return None
  
  # Returns memory address of variable
  def get_variable_address(self, var_name):
    if self.variable_exists(var_name):
      return self._variable_table[var_name][3]
    return None

  # Returns type and memory address of variable
  def get_variable_type_address(self, var_name):
    if self.variable_exists(var_name):
      return self._variable_table[var_name][0], self._variable_table[var_name][3]
    return None, None
  
  # Returns array/matrix total amount of items
  # var_name_address can be address or var_name
  # var_name_address must exist in directory
  def get_array_size(self, var_name_address):
    var_name = self.fix_var_name(var_name_address)
    dimensions = self.get_variable_dimensions(var_name)    
    array_size = 1
    for dimension in dimensions:
      array_size *= dimension
    return array_size

  # Returns amount of dimensions of variable
  # var_name_address can be address or var_name
  # var_name_address must exist in directory
  def get_array_dimensions_count(self, var_name_address):
    var_name = self.fix_var_name(var_name_address)
    dimensions = self.get_variable_dimensions(var_name)        
    return len(dimensions)

  # Returns indexed variable dimension
  # var_name_address must exist in directory
  def get_variable_dimension(self, var_name_address, index):
    var_name = self.fix_var_name(var_name_address)
    dimensions = self.get_variable_dimensions(var_name)
    if index >= len(dimensions):
      return None
    return dimensions[index]

  # Returns var_name of var_name_address
  # var_name_address must exist in directory
  # var_name_address can be address or var_name
  def fix_var_name(self, var_name_address):
    # Check if var_name_address is an address
    if isinstance(var_name_address, int):
      var_name_address = self.get_var_name_from_address(var_name_address)
    return var_name_address

  # Returns var_name of address
  # address must exist in directory
  def get_var_name_from_address(self, address):
    for var_name in self._variable_table.keys():
      if address == self.get_variable_address(var_name):
        return var_name

  # Returns amount of memory used by variable
  # var_name must exist in directory
  def get_variable_size(self, var_name):
    return 1 if not self.is_array(var_name) else self.get_array_size(var_name)

  # Returns total amount of memory used in variable directory by type
  def get_memory_size_by_type(self):
    memory_sizes = {type:0 for type in Types.primitives}
    for var_name in self._variable_table.keys():
      size = self.get_variable_size(var_name)
      type = self.get_variable_type(var_name)
      memory_sizes[type] += size
    return memory_sizes

  # Adds a variable to dictionary
  # Type, is_public, array_dimensions, memory_address
  def add_variable(self, var_name, type, is_public, memory_address):
    if var_name in self._variable_table:
      helpers.throw_error('Variable ' + var_name + ' already defined in scope.')
    self._variable_table[var_name] = [type, is_public, [], memory_address]

  # Adds a dimension to variable, used for arrays and matrices
  def add_dimension(self, var_name, dimension_size):
    self.get_variable_dimensions(var_name).append(dimension_size)

  # Checks if variable is an array or matrix
  def is_array(self, var_name):
    return len(self.get_variable_dimensions(var_name)) > 0

  # Checks if variable exists in directory
  def variable_exists(self, var_name):
    return var_name in self._variable_table.keys()

  # Used for debugging and testing purposes
  def print(self):
    print("Vars:")
    for key, value in self._variable_table.items():
      print(key, '\t', value[0], '\t', value[1], '\t', value[2], '\t', value[3])

class FunctionDirectory:
  # Initializes object with empty dictionary
  # Adds global block when created
  # Each value will be [Type, directory, is_public]
  def __init__(self):
    self._function_table = {}
    self.add_block(Constants.GLOBAL_BLOCK)

  # Return type stored in dictionary entry
  def get_entry_type(self, block_name):
    return self._function_table[block_name][0]

  # Return directory stored in dictionary entry
  def get_entry_directory(self, block_name):
    return self._function_table[block_name][1]

  # Returns type, address, block, class of var_name
  # Checks on all possible scopes
  def get_variable_item_deep(self, var_name, block_name, class_name, throw_error = True):
    # Glocal scope
    if block_name == Constants.GLOBAL_BLOCK and class_name is None:
      type_, address_ = self.get_entry_directory(block_name).get_variable_type_address(var_name)
      block_ = Constants.GLOBAL_BLOCK
      class_ = None
      if throw_error and address_ is None:
        helpers.throw_error('Undeclared variable ' + var_name)
      return type_, address_, block_, class_

    # funcion global
    if class_name is None:
      type_, address_ = self.get_entry_directory(block_name).get_variable_type_address(var_name)
      block_ = block_name
      class_ = None
    # metodo de una clase
    else:
      # esto busca en los locales del metodo y en los atributos
      type_, address_, block_, class_ = self.get_entry_directory(class_name).get_variable_item_deep(var_name, block_name, None, False)
      class_ = class_name
    
    if address_ is not None:
      return type_, address_, block_, class_

    return self.get_variable_item_deep(var_name, Constants.GLOBAL_BLOCK, None, throw_error)

  # Returns type of var_name
  # Checks on all possible scopes
  def get_variable_type_deep(self, var_name, block_name, class_name, throw_error = True):
    return self.get_variable_item_deep(var_name, block_name, class_name, throw_error)[0]

  # Returns address of var_name
  # Checks on all possible scopes
  def get_variable_address_deep(self, var_name, block_name, class_name, throw_error = True):
    return self.get_variable_item_deep(var_name, block_name, class_name, throw_error)[1]

  # Checks if block exists in function table
  def block_exists(self, block_name):
    return block_name in self._function_table.keys()

  # Adds a block to dictionary
  def add_block(self, block_name, type = None, is_public = None, class_name = None):
    # Adding block to main function directory
    if class_name is None:
      # Class block has a function directory
      if type == Constants.CLASS_BLOCK:
        if self.block_exists(block_name):
          helpers.throw_error('Class ' + block_name + ' is already defined.')
        directory = FunctionDirectory()
      # Other blocks have a variable directory
      else:
        if self.block_exists(block_name):
          helpers.throw_error('Function ' + block_name + ' already defined in scope.')
        directory = VariableDirectory()
      # Adds block to main function directory
      self._function_table[block_name] = [type, directory, is_public]
    # Adding block to function directory of class
    else:
      # Check if constructor is named as class
      if type == Constants.CONSTRUCTOR_BLOCK and block_name != class_name:
        helpers.throw_error('Constructor in ' + class_name + ' should be named as class.')
      self.get_entry_directory(class_name).add_block(block_name, type, is_public)

  # Checks if class exists in function directory
  def check_class_exists(self, class_name):
    if not self.block_exists(class_name):
      helpers.throw_error('Class ' + class_name + ' is not defined.')

  # Method used to execute similar code in multiple methods
  def common_method(self, method_name, positional_arguments, block_name, class_name = None):
    if class_name == None:
      method = getattr(VariableDirectory, method_name)
      directory = self.get_entry_directory(block_name)
      return method(directory, *positional_arguments)
    else:
      method = getattr(FunctionDirectory, method_name)
      directory = self.get_entry_directory(class_name)
      positional_arguments.insert(1, block_name)
      return method(directory, *positional_arguments)

  # Adds a variable to a VariableDirectory of a block
  def add_variable(self, var_name, block_name, type, is_public, memory_address, class_name = None):
    self.common_method("add_variable",
                       [var_name, type, is_public, memory_address],
                       block_name, class_name)
  
  # Se movio block_name de posicion
  # Adds a dimension to a variable
  def add_dimension(self, var_name, block_name, dimension_size, class_name = None):
    self.common_method("add_dimension",
                       [var_name, dimension_size],
                       block_name, class_name)

  # Return size of an array
  def get_array_size(self, var_name, block_name, class_name = None):
    return self.common_method("get_array_size",
                              [var_name],
                              block_name, class_name)

  # Se movio block_name de posicion
  # Returns indexed dimension of variable
  def get_variable_dimension(self, var_name_address, block_name, index, class_name = None):
    return self.common_method("get_variable_dimension",
                              [var_name_address, index],
                              block_name, class_name)

  # Returns amount of dimensions of variable
  def get_array_dimensions_count(self, var_name_address, block_name, class_name = None):
    return self.common_method("get_array_dimensions_count",
                              [var_name_address],
                              block_name, class_name)

  # Returns var_name of address
  def get_var_name_from_address(self, memory_address, block_name, class_name = None):
    return self.common_method("get_var_name_from_address",
                              [memory_address],
                              block_name, class_name)

  # Returns total amount of memory used in variable directory of a class
  def get_class_variables_memory_size(self, class_name):
    return self.get_entry_directory(class_name). \
           get_entry_directory(Constants.GLOBAL_BLOCK).get_memory_size_by_type()

  # Return type of subroutine
  def get_sub_type(self, block_name, class_name = None):
    if class_name == None:
      return self.get_entry_type(block_name)
    else:
      return self.get_entry_directory(class_name).get_sub_type(block_name)

  # Deletes a subroutine from directory
  def free_memory(self, block_name, class_name = None):
    if class_name is None:
      self._function_table.pop(block_name)
    else:
      self.get_entry_directory(class_name).free_memory(block_name)

  # Checks if given name is a class
  def is_class(self, class_name):
    return class_name in self._function_table.keys() and \
           self.get_entry_type(class_name) == Constants.CLASS_BLOCK

  # Checks if attribute exists in class
  def attribute_exists(self, var_name, class_name):
    return self.get_entry_directory(class_name). \
           get_entry_directory(Constants.GLOBAL_BLOCK). \
           variable_exists(var_name)
  
  # Checks if attribute in class is public
  def is_attribute_public(self, var_name, class_name):
    return self.get_entry_directory(class_name). \
           get_entry_directory(Constants.GLOBAL_BLOCK). \
           get_variable_is_public(var_name)

  # Used for debugging and testing purposes
  def output(self):
    print("------------------------------")
    print("|     FUNCTION DIRECTORY     |")
    print("------------------------------")
    print("xyz_name : name | type is_public")
    print("v_name\ttype\tis_public\tdims")
    print("------------------------------")
    self.print()
    print("|   END FUNCTION DIRECTORY   |")
    print("------------------------------")
    self._function_table.clear()

  # Used for debugging and testing purposes
  def print(self):
    for key, value in self._function_table.items():
      if value[0] == Constants.CLASS_BLOCK:
        print("|    CLASS_BLOCK    |")
        print("--------------------")
      print("block_name", ":" , key, "|", value[0], value[2])
      if value[0] == Constants.CLASS_BLOCK:
        print("------------------------------")
      value[1].print()
      if value[0] != Constants.CLASS_BLOCK:
        print("------------------------------")
      else:
        print("|  END CLASS_BLOCK  |")
        print("------------------------------")
