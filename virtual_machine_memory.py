from constants import Types, Defaults, MemoryRanges, MemoryTypes
from structures import Stack
import helpers

class VirtualMachineMemoryPointerMap:
  def __init__(self):
    self._pointers = []
  
class VirtualMachineMemoryPrimitivesMap:
  def __init__(self):
    setattr(self, Types.INT, [])
    setattr(self, Types.FLT, [])
    setattr(self, Types.STR, [])
    setattr(self, Types.BOOL, [])
  
  def fill(self, new_address, type):
    current_size = len(getattr(self, type))
    if new_address < current_size:
      return
    default_value = getattr(Defaults, type.upper())
    for _ in range(new_address - current_size + 1):
      getattr(self, type).append(default_value)

  def get_memory_address_type(self, memory_address):
    for current_type in Types.primitives:
      upper_type = current_type.upper()
      if memory_address >= getattr(MemoryRanges, upper_type) and  memory_address < getattr(MemoryRanges, upper_type + '_MAX'): 
        type = current_type
    
    new_address = memory_address - getattr(MemoryRanges, type.upper())
    return new_address, type

  def get_memory_value(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    self.fill(new_address, type)
    value = getattr(self, type)[new_address]
    if value is None:
      helpers.throw_error_no_line("Error: variable referenced before assignment")
    return value
  
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

  def get_memory_value(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    if type == MemoryTypes.POINTERS:
      return getattr(self, MemoryTypes.POINTERS)[new_address]
    return getattr(self, type).get_memory_value(new_address)
  
  def set_memory_value(self, memory_address, value):
    new_address, type = self.get_memory_address_type(memory_address)
    getattr(self, type).set_memory_value(new_address, value)
  
  def set_address_to_pointer(self, memory_address, value):
    new_address = self.get_memory_address_type(memory_address)[0]
    pointers = getattr(self, MemoryTypes.POINTERS)
    self.fill_pointers(new_address)
    pointers[new_address] = value

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
          value = bool(value)
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

    # if type != MemoryTypes.LOCAL:
    upper_type = type.upper()
    new_address = memory_address - getattr(MemoryRanges, upper_type)
    # TODO: else

    return new_address, type

  def get_memory_value(self, memory_address, read_address = False):
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and self.get_current_attr(type).is_pointer(new_address):
      stored_address = self.get_current_attr(type).get_memory_value(new_address)
      if read_address:
        return stored_address
      return self.get_memory_value(stored_address)
    return self.get_current_attr(type).get_memory_value(new_address)
  
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
    return self.get_current_attr(type).get_memory_type(new_address)

  def new_local_memory(self, sub_call):
    local_memory = VirtualMachineMemoryScopeMap()
    # sub_call -> [goto, params, return_temporal_address, return_quad_position]
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
  
  def get_return_position(self):
    return self._execution_stack.top()[0][3]
  
  def get_return_temporal_address(self):
    return self._execution_stack.top()[0][2]

  def pop_local_memory(self):
    self._execution_stack.pop()
  