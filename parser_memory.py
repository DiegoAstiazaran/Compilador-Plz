from constants import MemoryRanges, Types, MemoryTypes, Constants
import helpers

# this is one of the main parser memory structures, it keeps the addresses
# for all primitive type variables
class ParserMemoryPrimitivesMap:
  def __init__(self, first_class, second_class = None):
    self._first = first_class
    self._second = second_class
    base_address = getattr(MemoryRanges, first_class.upper())
    if second_class is not None:
      base_address += getattr(MemoryRanges, second_class.upper())

    if first_class == MemoryTypes.ATTRIBUTES:
      for type in Types.primitives:
        setattr(self, type, base_address)
        upper_size = type.upper() + '_SIZE'
        setattr(self, type + '_max', base_address + getattr(MemoryRanges, upper_size))

      return

    for type in Types.primitives:
      # start
      setattr(self, type, base_address + getattr(MemoryRanges, type.upper()))
      # max, can't get to this number
      type_max = type + '_max'
      setattr(self, type_max, base_address + getattr(MemoryRanges, type_max.upper()))

  # gets the next address memory for a given type
  def get_next(self, type):
    if type not in Types.primitives: # When getting memory for objects
      directions = {}
      for type in Types.primitives:
        directions[type] = self.get_next_no_increase(type)
      return directions
    actual = getattr(self, type)
    if actual == getattr(self, type + '_max') - 1:
      helpers.throw_error_no_line("Out of memory")
    setattr(self, type, actual + 1)
    return actual
  
  # gets the next available address without increasing the counter
  def get_next_no_increase(self, type):
    return getattr(self, type)
  
  # increases the counter of the address count for a given type.
  def increase_counter(self, type, amount):
    actual = getattr(self, type)
    setattr(self, type, actual + amount)
  
  # resets all memory structures
  def reset(self):
    ParserMemoryPrimitivesMap.__init__(self, self._first, self._second)

# Memory for constants for runtime
class ParserMemoryConstantMap(ParserMemoryPrimitivesMap):
  def __init__(self):
    ParserMemoryPrimitivesMap.__init__(self, MemoryTypes.CONSTANTS)
    self._memory = {type:{} for type in Types.primitives}

  # get the memory address of a given value and type
  def get_memory_address(self, value, type):
    if value in self._memory[type].keys() :
      return self._memory[type][value]
    new_address = self.get_next(type)
    self._memory[type][value] = new_address
    return new_address
  
  def get_map(self):
    return self._memory
  
  # get the value of a constant from a given address and type.
  def get_constant_from_address(self, address, type):
    constants_map = self._memory[type]
    for constant, const_address in constants_map.items():
      if address == const_address:
        return constant

class ParserMemoryManagerScopeMap:
  def __init__(self, scope_type): # Global, Local
    # Main variables
    scope = ParserMemoryPrimitivesMap(scope_type, MemoryTypes.SCOPE)
    setattr(self, MemoryTypes.SCOPE, scope)

    # Temporal variables
    temporal = ParserMemoryPrimitivesMap(scope_type, MemoryTypes.TEMPORAL)
    setattr(self, MemoryTypes.TEMPORAL, temporal)
    
    # Pointer variables, only counter
    upper_scope_type = scope_type.upper()
    pointers = getattr(MemoryRanges, upper_scope_type) + MemoryRanges.POINTERS
    setattr(self, MemoryTypes.POINTERS, pointers)
    # To reset pointers
    self.pointers_start = getattr(self, MemoryTypes.POINTERS)
    self.pointers_max = getattr(self, MemoryTypes.POINTERS) + MemoryRanges.POINTERS_SIZE

  def get_memory_map(self, in_scope_type):
    return getattr(self, in_scope_type)
  
  # get the next pointer address
  def get_next_pointer(self):
    actual = getattr(self, MemoryTypes.POINTERS)
    if actual == self.pointers_max - 1:
      helpers.throw_error_no_line("Out of memory")
    setattr(self, MemoryTypes.POINTERS, actual + 1)
    return actual
  
  # reset all the memory structures
  def reset(self):
    getattr(self, MemoryTypes.SCOPE).reset()
    getattr(self, MemoryTypes.TEMPORAL).reset()
    setattr(self, MemoryTypes.POINTERS, self.pointers_start)

class ParserMemoryManager:
  def __init__(self):
    constants = ParserMemoryConstantMap()
    setattr(self, MemoryTypes.CONSTANTS, constants)

    global_ = ParserMemoryManagerScopeMap(MemoryTypes.GLOBAL)
    setattr(self, MemoryTypes.GLOBAL, global_)
    local = ParserMemoryManagerScopeMap(MemoryTypes.LOCAL)
    setattr(self, MemoryTypes.LOCAL, local)

    attributes = ParserMemoryPrimitivesMap(MemoryTypes.ATTRIBUTES)
    setattr(self, MemoryTypes.ATTRIBUTES, attributes)

  def get_scope_type(self, current_block, current_class):
    if current_block == Constants.GLOBAL_BLOCK and current_class == None: # global
      return MemoryTypes.GLOBAL
    elif current_class == None: # global subroutine
      return MemoryTypes.LOCAL
    else: # clase
      if current_block == Constants.GLOBAL_BLOCK: # attribute
       return MemoryTypes.ATTRIBUTES
      else: # class subroutine
        return MemoryTypes.LOCAL

  # var_type: primitives
  # in_scope_type : scope, temporal
  def get_memory_address(self, var_type, in_scope_type, current_block, current_class):
    memory_scope = self.get_scope_type(current_block, current_class)
    if memory_scope == MemoryTypes.ATTRIBUTES:
      return getattr(self, memory_scope).get_next(var_type)
    return getattr(self, memory_scope).get_memory_map(in_scope_type).get_next(var_type)

  # Returns address that corresponds to a constant
  def get_constant_memory_address(self, value, type):
    return getattr(self, MemoryTypes.CONSTANTS).get_memory_address(value, type)
  
  # Returns constant value from an address
  def get_constant_from_address(self, address, type):
    return getattr(MemoryTypes.CONSTANTS).get_constant_from_address(address, type)
 
  # used only for arrays which are in scope type
  # memory_scope: global, local, attributes
  def increase_counter(self, type, amount, current_block, current_class):
    memory_scope = self.get_scope_type(current_block, current_class)
    scope_map = getattr(self, memory_scope)
    # always increase main in_scope variables, not temporals or pointers
    primitives_map = scope_map if memory_scope == MemoryTypes.ATTRIBUTES else \
                     getattr(scope_map, MemoryTypes.SCOPE)
    primitives_map.increase_counter(type, amount)

  # get the next pointer address for this memory manager structure
  def get_next_pointer(self, current_block, current_class):
    memory_scope = self.get_scope_type(current_block, current_class)
    return getattr(self, memory_scope).get_next_pointer()

  # get the complete structure of memory for constants.
  def get_constants_map(self):
    return getattr(self, MemoryTypes.CONSTANTS).get_map()

  def reset_local(self): # para el local cada que empieces una funcion o metodo
    getattr(self, MemoryTypes.LOCAL).reset()
  
  def reset_class(self): # cuando declaras una clase
    getattr(self, MemoryTypes.ATTRIBUTES).reset()
