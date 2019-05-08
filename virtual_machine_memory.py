from constants import Constants, Types, Defaults, MemoryRanges, MemoryTypes
from structures import Stack
import helpers

class VirtualMachineMemoryPrimitivesMap:
  def __init__(self):
    setattr(self, Types.INT, [])
    setattr(self, Types.FLT, [])
    setattr(self, Types.STR, [])
    setattr(self, Types.BOOL, [])
  
  # fill the memory with its default values
  def fill(self, new_address, type):
    current_size = len(getattr(self, type))
    if new_address < current_size:
      return
    default_value = getattr(Defaults, type.upper())
    for _ in range(new_address - current_size + 1):
      getattr(self, type).append(default_value)

  # get the type of a given memory address, it can be constant, a primitive type, scope, etc. 
  def get_memory_address_type(self, memory_address):
    for current_type in Types.primitives:
      upper_type = current_type.upper()
      if memory_address >= getattr(MemoryRanges, upper_type) and  memory_address < getattr(MemoryRanges, upper_type + '_MAX'): 
        type = current_type
    
    new_address = memory_address - getattr(MemoryRanges, type.upper())
    return new_address, type

  # get the value of a varibale given the address. 
  def get_memory_value(self, memory_address, return_none = False):
    new_address, type = self.get_memory_address_type(memory_address)
    self.fill(new_address, type)
    value = getattr(self, type)[new_address]
    if value is None and not return_none:
      helpers.throw_error_no_line("Error: variable referenced before assignment")
    return value
  
  # set an address to a given value
  def set_memory_value(self, memory_address, value):
    new_address, type = self.get_memory_address_type(memory_address)
    self.fill(new_address, type)
    getattr(self, type)[new_address] = value

  def get_memory_type(self, memory_address):
    _, type = self.get_memory_address_type(memory_address)
    return type

class VirtualMachineMemoryScopeMap:
  def __init__(self):
    setattr(self, MemoryTypes.SCOPE, VirtualMachineMemoryPrimitivesMap())
    setattr(self, MemoryTypes.TEMPORAL, VirtualMachineMemoryPrimitivesMap())
    setattr(self, MemoryTypes.POINTERS, [])
  
  def get_memory_address_type(self, memory_address):
    if memory_address >= MemoryRanges.SCOPE and  memory_address < MemoryRanges.SCOPE_MAX:
      type = MemoryTypes.SCOPE
    elif memory_address >= MemoryRanges.TEMPORAL and  memory_address < MemoryRanges.TEMPORAL_MAX:
      type = MemoryTypes.TEMPORAL
    elif memory_address >= MemoryRanges.POINTERS and  memory_address < MemoryRanges.POINTERS_MAX:
      type = MemoryTypes.POINTERS 
    
    upper_type = type.upper()
    new_address = memory_address - getattr(MemoryRanges, upper_type)
    return new_address, type
  
  def get_type(self, memory_address):
    return self.get_memory_address_type(memory_address)[1]

  # get the value from a given address.
  def get_memory_value(self, memory_address, return_none = False):
    new_address, type = self.get_memory_address_type(memory_address)
    if type == MemoryTypes.POINTERS:
      self.fill_pointers(new_address)
      return getattr(self, MemoryTypes.POINTERS)[new_address]
    return getattr(self, type).get_memory_value(new_address, return_none)
  
  # set the value of a given address
  def set_memory_value(self, memory_address, value):
    new_address, type = self.get_memory_address_type(memory_address)
    getattr(self, type).set_memory_value(new_address, value)
  
  def set_address_to_pointer(self, memory_address, value):
    new_address = self.get_memory_address_type(memory_address)[0]
    pointers = getattr(self, MemoryTypes.POINTERS)
    self.fill_pointers(new_address)
    pointers[new_address] = value

  # fill the existing pointers with its default values.
  def fill_pointers(self, new_address):
    pointers = getattr(self, MemoryTypes.POINTERS)
    current_size = len(pointers)
    if new_address < current_size:
      return
    default_value = None
    for _ in range(new_address - current_size + 1):
      pointers.append(default_value)

  def is_pointer(self, memory_address):
    return memory_address >= MemoryRanges.POINTERS and memory_address < MemoryRanges.POINTERS_MAX

  def get_memory_type(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_type(new_address)

class VirtualMachineMemoryManager:
  def __init__(self):
    setattr(self, MemoryTypes.GLOBAL, VirtualMachineMemoryScopeMap())
    setattr(self, MemoryTypes.CONSTANTS, VirtualMachineMemoryPrimitivesMap())
    self._execution_stack = Stack() # For local memory
    self._pending_execution_stack = Stack()
  
  def get_current_attr(self, type):
    if type == MemoryTypes.LOCAL:
      return self.get_current_local_memory()
    return getattr(self, type)

  # attribute is an object of ConstantMemoryManager that comes from compilation
  # called only once
  def add_constant_memory(self, constants_map):
    for type, type_map in constants_map.items():
      for value, address in type_map.items():
        if type ==  Types.BOOL:
          value = value == Constants.TRUE
        getattr(self, MemoryTypes.CONSTANTS).set_memory_value(address, value)

  def get_memory_address_type(self, memory_address):
    if memory_address >= MemoryRanges.CONSTANTS and memory_address < MemoryRanges.CONSTANTS_MAX:
      type = MemoryTypes.CONSTANTS
    elif memory_address >= MemoryRanges.GLOBAL and memory_address <= MemoryRanges.GLOBAL_MAX:
      type = MemoryTypes.GLOBAL
    elif memory_address >= MemoryRanges.LOCAL and memory_address <= MemoryRanges.LOCAL_MAX:
      type = MemoryTypes.LOCAL
    else:
      helpers.throw_error_no_line("Error in address")

    upper_type = type.upper()
    new_address = memory_address - getattr(MemoryRanges, upper_type)

    return new_address, type

  def get_memory_value(self, memory_address, read_address = False, return_none = False):
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and self.get_current_attr(type).is_pointer(new_address):
      stored_address = self.get_current_attr(type).get_memory_value(new_address)
      if read_address:
        return stored_address
      return self.get_memory_value(stored_address)
    return self.get_current_attr(type).get_memory_value(new_address, return_none)
  
  def set_memory_value(self, memory_address, value, assign_address = False):
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and self.get_current_attr(type).is_pointer(new_address):
      if assign_address:
        self.get_current_attr(type).set_address_to_pointer(new_address, value)
        return
      stored_address = self.get_current_attr(type).get_memory_value(new_address)
      self.set_memory_value(stored_address, value)
      return
    self.get_current_attr(type).set_memory_value(new_address, value)

  def get_memory_type(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and self.get_current_attr(type).is_pointer(new_address):
      memory_address = self.get_current_attr(type).get_memory_value(new_address)
      new_address, type = self.get_memory_address_type(memory_address)
    return self.get_current_attr(type).get_memory_type(new_address)

  def new_local_memory(self, sub_call):
    local_memory = VirtualMachineMemoryScopeMap()
    # sub_call -> [goto, params, variables_sizes, return_temporal_address, return_quad_position]
    self._pending_execution_stack.push([sub_call, local_memory])
  
  def get_current_local_memory(self):
    return self._execution_stack.top()[1]
  
  def get_next_local_memory(self):
    return self._pending_execution_stack.top()[1]

  def get_sub_call(self):
    return self._pending_execution_stack.top()[0]
  
  def get_sub_call_arg_address(self, param_counter):
    sub_call = self.get_sub_call()
    return sub_call[1][param_counter].get_value()

  def get_sub_call_start(self):
    sub_call = self.get_sub_call()
    return sub_call[0]

  def set_arg_value(self, memory_address, value):
    local_memory = self.get_next_local_memory()
    new_address = self.get_memory_address_type(memory_address)[0]
    local_memory.set_memory_value(new_address, value)
  
  def set_quad_pointer(self, quad_pointer):
    self._pending_execution_stack.top()[0].append(quad_pointer)
  
  def set_new_local_memory(self):
    local_memory = self._pending_execution_stack.pop()
    self._execution_stack.push(local_memory)

  def get_local_variable_sizes(self):
    return self._execution_stack.top()[0][2]

  def get_return_temporal_address(self):
    return self._execution_stack.top()[0][3]

  def get_return_position(self):
    return self._execution_stack.top()[0][4]

  def pop_local_memory(self):
    self._execution_stack.pop()
  
  def get_address_for_list(self, list_address, list_type, global_addresses):
    _, type = self.get_memory_address_type(list_address)
    type_index = Types.primitives.index(list_type)
    if type == MemoryTypes.GLOBAL:
      current = global_addresses[type_index]
      global_addresses[type_index] += 1
      return current
    elif type == MemoryTypes.LOCAL:
      current = self.get_local_variable_sizes()[type_index]
      self.get_local_variable_sizes()[type_index] += 1
  
  def new_list_node(self, list_address, list_type, global_addresses):
    next_block_address = self.get_address_for_list(list_address, list_type, global_addresses)
    next_block_address_pointer = self.get_address_for_list(list_address, list_type, global_addresses)
    return next_block_address, next_block_address_pointer
  
  #
  def list_set_next(self, current_address, next_address):
    new_address, type = self.get_memory_address_type(current_address)
    if not self.get_current_attr(type).is_pointer(new_address):
      current_address += 1
    self.set_memory_value(current_address, next_address, assign_address = True)

  # get the next element of a list. 
  def list_get_next(self, current_address):
    new_address, type = self.get_memory_address_type(current_address)
    if not self.get_current_attr(type).is_pointer(new_address):
      current_address += 1
    return self.get_memory_value(current_address, read_address=True, return_none=True)

  # append an element to a list.
  def list_append_node(self, list_address, list_type, value, global_addresses):
    next_block_address, next_block_address_pointer = self.new_list_node(list_address, list_type, global_addresses)

    prev_address = list_address
    current_address = self.list_get_next(list_address)
    while current_address is not None:
      prev_address = current_address
      current_address = self.list_get_next(current_address)
    self.list_set_next(prev_address, next_block_address)
    self.set_memory_value(next_block_address, value)
    self.set_memory_value(next_block_address_pointer, None)

  # get all the items from a given list.
  def list_get_items(self, list_address):
    current_address = self.list_get_next(list_address)
    list_values = []
    while current_address is not None:
      current_node_value = self.get_memory_value(current_address)
      list_values.append(current_node_value)
      current_address = self.list_get_next(current_address)
    return list_values
  
  # pop a value from a list, given an index
  def list_pop_node(self, list_address, index):
    if index < 0:
      helpers.throw_error_no_line("Index must receive a positive integer as argument.")
    prev_address = list_address
    current_address = self.list_get_next(list_address)
    while current_address is not None and index > 0:
      prev_address = current_address
      current_address = self.list_get_next(current_address)
      index -= 1
    
    if current_address is None:
      helpers.throw_error_no_line("Not enough elements in list.")

    next_address = self.list_get_next(current_address)
    self.list_set_next(prev_address, next_address)

    pop_value = self.get_memory_value(current_address)
    return pop_value
  
  # Return value at given index
  def list_index_node(self, list_address, index):
    if index < 0:
      helpers.throw_error_no_line("Index must receive a positive integer as argument.")
    current_address = self.list_get_next(list_address)
    while current_address is not None and index > 0:
      current_address = self.list_get_next(current_address)
      index -= 1
    if current_address is None:
      helpers.throw_error_no_line("Not enough elements in list for pop operation.")
    index_value = self.get_memory_value(current_address, return_none=True)
    return index_value
  
  # remove a value from list. 
  def list_remove_node(self, list_address, remove_value):
    prev_address = list_address
    current_address = self.list_get_next(list_address)
    while current_address is not None:
      current_value = self.get_memory_value(current_address)
      if current_value == remove_value:
        current_next = self.list_get_next(current_address)
        self.list_set_next(prev_address, current_next)
        current_address = current_next
      else:
        prev_address = current_address
        current_address = self.list_get_next(current_address)

  # insert a new value to a list. 
  def list_insert_node(self, list_address, index, value, list_type, global_addresses):
    prev_address = list_address
    current_address = self.list_get_next(list_address)
    while index > 0 and current_address is not None:
      prev_address = current_address
      current_address = self.list_get_next(current_address)
      index -= 1
    for _ in range(index + 1):
      new_address, new_address_pointer = self.new_list_node(list_address, list_type, global_addresses)
      self.set_memory_value(new_address, value)
      self.set_memory_value(new_address_pointer, None)
      self.list_insert_node_aux(prev_address, new_address, current_address)
      prev_address = new_address
  
  # Helper to change pointers when node in inserted
  def list_insert_node_aux(self, prev_address, new_address, next_address):
    self.list_set_next(prev_address, new_address)
    self.list_set_next(new_address, next_address)
  
  # reverse a list
  def list_reverse(self, list_address):
    prev_address = None
    current_address = self.list_get_next(list_address)
    while current_address is not None:
      next_address = self.list_get_next(current_address)
      self.list_set_next(current_address, prev_address)
      prev_address = current_address
      current_address = next_address
    self.list_set_next(list_address, prev_address)
    
