from constants import Constants
import helpers

# Stores variables for a block
# Includes name, type and if it is public in case of class
class VariableDirectory:
  # Initializes object with empty dictionary
  def __init__(self):
    self._variable_table = {}

  # Adds a variable to dictionary
  def add_variable(self, var_name, type, is_public):
    if var_name in self._variable_table:
      helpers.throw_error('Variable ' + var_name + ' already defined in scope.')
    self._variable_table[var_name] = [type, is_public, None]

  def add_dimension(self, var_name):
    self._variable_table[var_name][2] = 1 if self._variable_table[var_name][2] == None else 2

  # Used for debugging and testing purposes
  def print(self):
    print("Vars:")
    for key, value in self._variable_table.items():
      print(key, '\t', value[0], '\t', value[1], '\t', value[2])

  def get_variable_type(self, var_name):
    if var_name in self._variable_table:
      return self._variable_table[var_name][0]
    else:
      helpers.throw_error('Undeclared variable ' + var_name)

class FunctionDirectory:
  # Initializes object with empty dictionary
  # Adds global block when created
  def __init__(self):
    self._function_table = {}
    self.add_block(Constants.GLOBAL_BLOCK)

  # Return directory stored in dictionary entry
  def get_entry_directory(self, block_name):
    return self._function_table[block_name][1]

  # Return type stored in dictionary entry
  def get_entry_type(self, block_name):
    return self._function_table[block_name][0]

  # Adds a block to dictionary
  def add_block(self, block_name, type = None, is_public = None, class_name = None):
    # Adding block to main function directory
    if class_name == None:
      # Class block has a function directory
      if type == Constants.CLASS_BLOCK:
        if block_name in self._function_table:
          helpers.throw_error('Class ' + block_name + ' is already defined.')
        directory = FunctionDirectory()
      # Other blocks have a variable directory
      else:
        if block_name in self._function_table:
          helpers.throw_error('Block ' + block_name + ' already defined in scope.')
        directory = VariableDirectory()
      # Adds block to main function directory
      self._function_table[block_name] = [type, directory, is_public]
    # Adding block to function directory of class
    else:
      # Check if construcor is named as class
      if type == Constants.CONSTRUCTOR_BLOCK and block_name != class_name:
        helpers.throw_error('Constructor in ' + class_name + ' should be named as class.')
      self.get_entry_directory(class_name).add_block(block_name, type, is_public)

  # Adds a variable to a VariableDirectory of a block
  def add_variable(self, var_name, block_name, type, is_public, class_name = None):
    # Adding variable of a block of main function directory
    if class_name == None:
      self.get_entry_directory(block_name).add_variable(var_name, type, is_public)
    # Adding variable of a block of a class's function directory
    else:
      self.get_entry_directory(class_name).add_variable(var_name, block_name, type, is_public)

  def add_dimension_to_variable(self, var_name, block_name, class_name = None):
    if class_name == None:
      self.get_entry_directory(block_name).add_dimension(var_name)
    else:
      self.get_entry_directory(class_name).add_dimension_to_variable(var_name, block_name)

  def check_class(self, class_name):
    if class_name not in self._function_table:
      helpers.throw_error('Class ' + class_name + ' is not defined.')

  def get_variable_type(self, var_name, block_name, class_name = None):
    if class_name == None:
      return self.get_entry_directory(block_name).get_variable_type(var_name)
    else:
      return self.get_entry_directory(class_name).get_variable_type(var_name, block_name)

  def get_sub_type(self, block_name, class_name = None):
    if class_name == None:
      return self.get_entry_type(block_name)
    else:
      return self.get_entry_directory(class_name).get_sub_type(block_name)

  def free_memory(self, block_name, class_name = None):
    if class_name is None:
      self._function_table.pop(block_name)
    else:
      self.get_entry_directory(class_name).free_memory(block_name)

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

class ParamDirectory:
  def __init__(self):
    self._param_table = {}
  
  def add(self, subroutine_name, start, is_public):
    self._param_table[subroutine_name] = [start, [], is_public]
  
  def get_params(self, subroutine_name):
    return self._param_table[subroutine_name][1]
  
  def add_param(self, subroutine_name, type):
    self.get_params(subroutine_name).append(type)

  def check_sub_exists(self, subroutine_name):
    return subroutine_name in self._param_table
  
  def check_arg(self, type, index, subroutine_name):
    if index >= self.get_param_count(subroutine_name):
      helpers.throw_error("Call not valid, more arguments than expected")
    return self.get_params(subroutine_name)[index] == type
  
  def get_param_count(self, subroutine_name):
    return len(self.get_params(subroutine_name))
  
  def is_method_public(self, subroutine_name):
    return self._param_table[subroutine_name][2]

class SubroutineDirectory:
  def __init__(self):
    self._subroutine_directory = {}
    self.add_block(Constants.GLOBAL_BLOCK)
  
  def fix_sub_name(self, sub_name, class_name = None):
    if class_name != None:
      sub_name = "{}.{}".format(class_name, sub_name)
    return sub_name
  
  def add_block(self, block_name):
    self._subroutine_directory[block_name] = ParamDirectory()
  
  def add_subroutine(self, block_name, subroutine_name, start, is_public):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    self._subroutine_directory[block_name].add(subroutine_name, start, is_public)

  def add_param(self, subroutine_name, type, block_name):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    self._subroutine_directory[block_name].add_param(subroutine_name, type)

  def check_sub_exists(self, subroutine_name, block_name):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    return self._subroutine_directory[block_name].check_sub_exists(subroutine_name)
  
  def check_block_exists(self, block_name):
    return block_name in self._subroutine_directory
  
  def check_arg(self, type, index, subroutine_name, block_name):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    return self._subroutine_directory[block_name].check_arg(type, index, subroutine_name)
  
  def get_param_count(self, subroutine_name, block_name):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    return self._subroutine_directory[block_name].get_param_count(subroutine_name)
  
  def is_method_public(self, subroutine_name, block_name):
    return self._subroutine_directory[block_name].is_method_public(subroutine_name)