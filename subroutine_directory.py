from copy import deepcopy

from constants import Constants
import helpers

# Directory for params of subroutines
# [start, params, is_public, type]
class SubroutineParamDirectory:
  # Initializes object with empty dictionary
  def __init__(self):
    self._param_table = {}

  # Returns complete array of information of subroutine
  def get_subroutine(self, subroutine_name):
    return self._param_table[subroutine_name]

  # Returns start of subroutine
  def get_start(self, subroutine_name):
    return self._param_table[subroutine_name][0]

  # Returns params of subroutine
  def get_params(self, subroutine_name):
    return self._param_table[subroutine_name][1]

  # Return is_public of subroutine
  def is_public(self, subroutine_name):
    return self._param_table[subroutine_name][2]

  # Returns type of subroutine
  def get_type(self, subroutine_name):
    return self._param_table[subroutine_name][3]

  # Returns amount of params of subroutine
  def get_param_count(self, subroutine_name):
    return len(self.get_params(subroutine_name))
  
  # Returns type of an indexed param of subroutine
  def get_param_type(self, index, subroutine_name):
    return self.get_params(subroutine_name)[index].get_type()

  # Add param to subroutine
  # Param is an OperandPair
  def add_param(self, subroutine_name, param):
    self.get_params(subroutine_name).append(param)

  # Adds a subroutine to directory
  def add_subroutine(self, subroutine_name, start, is_public, type):
    self._param_table[subroutine_name] = [start, [], is_public, type]

  # Checks if subroutine exists in directory
  def subroutine_exists(self, subroutine_name):
    return subroutine_name in self._param_table.keys()
  
  # Checks argument against stored params
  def check_arg(self, arg_type, index, subroutine_name):
    if index >= self.get_param_count(subroutine_name):
      helpers.throw_error("Call not valid, more arguments than expected")
    return self.get_param_type(index, subroutine_name) == arg_type

  def add_next_memory_addresses(self, memory_addresses, subroutine_name):
    self._param_table[subroutine_name].append(memory_addresses)
  
  def get_next_memory_addresses(self, subroutine_name):
    return self._param_table[subroutine_name][4]

  # Removes is_public and type in list of each subroutine
  def fix_for_virtual_machine(self):
    for subroutine_details in self._param_table.values():
      del subroutine_details[3]
      del subroutine_details[2]

# Directory for headers of subroutines
class SubroutineDirectory:
  # Initializes object with empty dictionary
  # Adds global block when created
  def __init__(self):
    self._subroutine_directory = {}
    self.add_block(Constants.GLOBAL_BLOCK)
  
  def get_param_directory(self, block_name):
    return self._subroutine_directory[block_name][0]

  # Returns amount of params of subroutine
  def get_param_count(self, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    param_count = self.get_param_directory(block_name).get_param_count(subroutine_name)
    return param_count if block_name == Constants.GLOBAL_BLOCK else param_count - 4
  
  # Returns type of subroutine
  def get_type(self, subroutine_name, block_name):
    return self.get_param_directory(block_name).get_type(subroutine_name)
  
  # Returns type of an indexed param of subroutine
  def get_param_type(self, index, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    return self.get_param_directory(block_name).get_param_type(index, subroutine_name)
  
  # Returns complete array of information of subroutine
  def get_subroutine(self, subroutine_name, block_name):
    return self.get_param_directory(block_name).get_subroutine(subroutine_name)

  # Return is_public of subroutine
  def is_public(self, subroutine_name, block_name):
    return self.get_param_directory(block_name).is_public(subroutine_name)
  
  # Adds new block to directory
  def add_block(self, block_name):
    self._subroutine_directory[block_name] = [SubroutineParamDirectory()]
  
  # Adds a subroutine to directory
  def add_subroutine(self, block_name, subroutine_name, start_quad, is_public, type):
    block_name = self.fix_block_name(block_name)
    self.get_param_directory(block_name).add_subroutine(subroutine_name, start_quad, is_public, type)
  
  # Add param to subroutine
  # Param is an OperandItem
  def add_param(self, subroutine_name, param, block_name):
    block_name = self.fix_block_name(block_name)
    self.get_param_directory(block_name).add_param(subroutine_name, param)

  # Checks if subroutine exists in directory
  def subroutine_exists(self, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    return self.get_param_directory(block_name).subroutine_exists(subroutine_name)
  
  # Checks if block exists in directory
  def block_exists(self, block_name):
    return block_name in self._subroutine_directory
  
  # Checks argument against stored params
  def check_arg(self, arg_type, index, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    return self.get_param_directory(block_name).check_arg(arg_type, index, subroutine_name)

  def add_next_memory_addresses(self, addresses, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    self.get_param_directory(block_name).add_next_memory_addresses(addresses, subroutine_name)

  def add_next_memory_addresses_to_block(self, addresses, block_name):
    block_name = self.fix_block_name(block_name)
    self._subroutine_directory[block_name].append(addresses)
  
  # get memory addresses of a given rubroutine
  def get_memory_addresses(self, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    return self.get_param_directory(block_name).get_next_memory_addresses(subroutine_name)
  
  #get the memory address of a block
  def get_memory_addresses_of_block(self, block_name):
    block_name = self.fix_block_name(block_name)
    return self._subroutine_directory[block_name][1]

  # Changes block_name to Global if None
  def fix_block_name(self, block_name):
    if block_name is None:
      block_name = Constants.GLOBAL_BLOCK
    return block_name

  # Removes is_public and type in list of each subroutine
  def fix_for_virtual_machine(self):
    for block_name in self._subroutine_directory.keys():
      self.get_param_directory(block_name).fix_for_virtual_machine()

  def fix_param_count(self, param_count, subroutine_name, block_name):
    block_name = self.fix_block_name(block_name)
    return param_count if block_name == Constants.GLOBAL_BLOCK else param_count + 4

  # Copies the attributes and methods of a parent class into the child class.
  def inherit_class(self, sub_class, base_class):
    self._subroutine_directory[sub_class] = deepcopy(self._subroutine_directory[base_class])
