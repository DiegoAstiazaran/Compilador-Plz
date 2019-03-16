from constants import GLOBAL_BLOCK, CLASS_BLOCK

# Stores variables for a block
# Includes name, type and if it is public in case of class
class VariableDirectory:
  # Initializes object with empty dictionary
  def __init__(self):
    self._variable_table = {}

  # Adds a variable to dictionary
  def add_variable(self, var_name, type, is_public):
    if var_name in self._variable_table:
      raise Exception('Variable ' + var_name + ' already defined in scope.')
    self._variable_table[var_name] = [type, is_public]
  
  # Used for debugging and testing purposes
  def print(self):
    print("Vars:")
    for key, value in self._variable_table.items():
      print(key, '\t', value[0], '\t', value[1])

class FunctionDirectory:
  # Initializes object with empty dictionary
  # Adds global block when created
  def __init__(self):
    self._function_table = {}
    self.add_block(GLOBAL_BLOCK)

  # Adds a block to dictionary
  def add_block(self, block_name, type = None, is_public = None, class_name = None):
    # Adding block to main function directory
    if class_name == None:
      # Class block has a function directory
      if type == CLASS_BLOCK:
        if block_name in self._function_table:
          raise Exception('Class ' + block_name + ' is already defined.')
        directory = FunctionDirectory()
      # Other blocks have a variable directory
      else:
        if block_name in self._function_table:
          raise Exception('Block ' + block_name + ' already defined in scope.')
        directory = VariableDirectory()
      # Adds block to main function directory
      self._function_table[block_name] = [type, directory, is_public]
    # Adding block to function directory of class
    else:
      self._function_table[class_name][1].add_block(block_name, type, is_public)   

  # Adds a variable to a VariableDirectory of a block
  def add_variable(self, var_name, block_name, type, is_public, class_name = None):
    # Adding variable of a block of main function directory
    if class_name == None:
      self._function_table[block_name][1].add_variable(var_name, type, is_public)
    # Adding variable of a block of a class's function directory
    else:
      self._function_table[class_name][1].add_variable(var_name, block_name, type, is_public)

  # Used for debugging and testing purposes
  def output(self):
    print("------------------------------")
    print("|     FUNCTION DIRECTORY     |")
    print("------------------------------")
    print("xyz_name : name | type is_public")
    print("v_name\ttype\tis_public")
    print("------------------------------")
    self.print()
    print("|   END FUNCTION DIRECTORY   |")
    print("------------------------------")
    self._function_table.clear()
  
  # Used for debugging and testing purposes
  def print(self):
    for key, value in self._function_table.items():
      if value[0] == CLASS_BLOCK:
        print("|    CLASS_BLOCK    |")
        print("--------------------")
      print("block_name", ":" , key, "|", value[0], value[2])
      if value[0] == CLASS_BLOCK:
        print("------------------------------")
      value[1].print()
      if value[0] != CLASS_BLOCK:
        print("------------------------------")
      else:
        print("|  END CLASS_BLOCK  |")
        print("------------------------------")
