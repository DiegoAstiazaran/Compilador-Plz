class Dictionary:
  def __init__(self):
    self._dictionary = {}

class VariableDirectory:
    def __init__(self):
      self._variable_table = {}

    def add_variable(self, var_name, type, is_public, dimensions):
      self._variable_table[var_name] = [type, is_public, dimensions]

class FunctionDirectory:

  def __init__(self):
    self._function_table = {}


  def add_block(self, block_name, type = None):
    if type == "class":
      x = FunctionDirectory()
    else:
      x = VariableDirectory()

    self._function_table[block_name] = [type, x]

  def add_variable(self, block_name, var_name, type, is_public = None, dimensions = 0):
    self._function_table[block_name][1].add_variable(var_name, type, is_public, dimensions)
