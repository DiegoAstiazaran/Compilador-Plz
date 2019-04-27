from constants import Types, Operators, Constants, MemoryRanges, MemoryTypes, Defaults, QuadOperations
import helpers

# Pair of operand value and type
class OperandPair:
  def __init__(self, operand_value, operand_type):
    self._pair = (operand_value, operand_type)

  def __str__(self):
    return str(self._pair)

  def __repr__(self):
    return str(self._pair)

  def get_value(self):
    return self._pair[0]

  def get_type(self):
    return self._pair[1]

# Implementantion of stack
class Stack:
  def __init__(self):
    self._stack = []

  def __str__(self):
    return str(self._stack)

  def push(self, value):
    self._stack.append(value)

  # Pops and returns element
  def pop(self):
    top = self.top()
    self._stack.pop()
    return top

  def top(self):
    return self._stack[-1]

  def empty(self):
    return not self._stack

# List for quads
class QuadList:
  def __init__(self):
    self._quad_list = []

  def __str__(self):
    return '[\n' + ',\n'.join('{}'.format(item) for item in self._quad_list) + '\n]'

  def next(self):
    return len(self._quad_list)

  def size(self):
    return len(self._quad_list)

  def add(self, quad):
    self._quad_list.append(quad)

  def erase(self, index):
    self._quad_list.pop(index)

  def add_element_to_quad(self, index, element):
    self._quad_list[index].add_element(element)
  
  def get(self, index):
    return self._quad_list[index]

  def print_with_number(self):
    index = 0
    for item in self._quad_list:
      print('#{}\t{}'.format(index, item))
      index += 1
  
# Quad for intermediate code
class Quad:
  def __init__(self, instruction, first = None, second = None, third = None):
    if instruction is None:
      helpers.throw_error("Quad operator must be different from None")
    self._quad = [instruction]
    if first is not None:
      self._quad.append(first)
    if second is not None:
      self._quad.append(second)
    if third is not None:
      self._quad.append(third)

  def __repr__(self):
    return ' '.join(str(i) for i in filter(None.__ne__, self._quad))

  def add_element(self, element):
    self._quad.append(element)
  
  def get_operation(self):
    return self._quad[0]
  
  def get_items(self):
    if len(self._quad) > 2:
      return tuple(self._quad[1:])
    else:
      return self._quad[1]

# TODO: delete
# Temporal memory manager
class TemporalMemory:
  def __init__(self):
    self._next_available = 0

  def get_available(self):
    self._next_available += 1
    return 'temp_%d' % (self._next_available - 1)

class ParserMemoryPrimitivesMap:
  def __init__(self, first_class, second_class = None):
    base_address = getattr(MemoryRanges, first_class.upper())
    if second_class is not None:
      base_address += getattr(MemoryRanges, second_class.upper())

    setattr(self, Types.INT, base_address + MemoryRanges.INT)
    setattr(self, Types.FLT, base_address + MemoryRanges.FLT)
    setattr(self, Types.STR, base_address + MemoryRanges.STR)
    setattr(self, Types.BOOL, base_address + MemoryRanges.BOOL)

    self._first = first_class
    self._second = second_class

  def get_next(self, type):
    if type not in Types.primitives:
      return None
      # TODO: use this error when constructors work
      # helpers.throw_error("Type must be a primitive")
    actual = getattr(self, type)
    setattr(self, type, actual + 1)
    return actual
  
  def increase_counter(self, type, amount):
    actual = getattr(self, type)
    setattr(self, type, actual + amount)
  
  def reset(self):
    ParserMemoryPrimitivesMap.__init__(self, self._first, self._second)

class ParserMemoryConstantMap(ParserMemoryPrimitivesMap):
  def __init__(self):
    ParserMemoryPrimitivesMap.__init__(self, MemoryTypes.CONSTANTS)
    self._memory = {type:{} for type in Types.primitives}

  def get_memory_address(self, value, type):
    if value in self._memory[type]:
      return self._memory[type][value]
    new_address = self.get_next(type)
    self._memory[type][value] = new_address
    return new_address
  
  def get_map(self):
    return self._memory
  
  def get_constant_from_address(self, address, type):
    constants = self._memory[type]
    for constant, const_address in constants.items():
      if address == const_address:
        return constant

class ParserMemoryManagerScopeMap:
  def __init__(self, type): # Global, Local
    scope = ParserMemoryPrimitivesMap(type, MemoryTypes.SCOPE)
    setattr(self, MemoryTypes.SCOPE, scope)
    temporal = ParserMemoryPrimitivesMap(type, MemoryTypes.TEMPORAL)
    setattr(self, MemoryTypes.TEMPORAL, temporal)
    upper_type = type.upper()
    pointers = getattr(MemoryRanges, upper_type) + MemoryRanges.POINTERS
    setattr(self, MemoryTypes.POINTERS, pointers)
    self.pointers_start = getattr(self, MemoryTypes.POINTERS)

  def get_memory_map(self, memory_type):
    return getattr(self, memory_type)
  
  def get_next_pointer(self):
    actual = getattr(self, MemoryTypes.POINTERS)
    setattr(self, MemoryTypes.POINTERS, actual + 1)
    return actual
  
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

  # var_type: primitives
  # memory_type : scope, temporal, pointers
  def get_memory_address(self, var_type, memory_type, current_block, current_class):
    if current_block == Constants.GLOBAL_BLOCK and current_class == None: # global
      memory_scope = MemoryTypes.GLOBAL
    elif current_class == None: # funcion
      memory_scope = MemoryTypes.LOCAL
    else: # clase
      if current_block == None: # attribute
        memory_scope = MemoryTypes.ATTRIBUTES
      else: # metodo
        memory_scope = MemoryTypes.LOCAL

    return getattr(self, memory_scope).get_memory_map(memory_type).get_next(var_type)

  def get_constant_memory_address(self, value, type):
    return getattr(self, MemoryTypes.CONSTANTS).get_memory_address(value, type)
  
  def get_constant_from_address(self, address, type):
    return getattr(MemoryTypes.CONSTANTS).get_constant_from_address(address, type)

  def get_last_global(self, type):
    global_ = getattr(self, MemoryTypes.GLOBAL)
    global_scope = getattr(global_, MemoryTypes.SCOPE)
    return getattr(global_scope, type) - 1
  
  # used only for arrays which are in scope type
  def increase_counter(self, type, memory_scope, amount):
    scope_map = getattr(self, memory_scope)
    getattr(scope_map, MemoryTypes.SCOPE).increase_counter(type, amount)

  def get_next_temporal(self, type, memory_scope):
    scope_map = getattr(self, memory_scope)
    return getattr(scope_map, MemoryTypes.TEMPORAL).get_next(type)

  def get_next_pointer(self, memory_scope):
    return getattr(self, memory_scope).get_next_pointer()

  def get_constant_map(self):
    return getattr(self, MemoryTypes.CONSTANTS)

  def reset_local(self): # para el local cada que empieces una funcion o metodo
    getattr(self, MemoryTypes.LOCAL).reset()
  
  def reset_class(self): # cuando declaras una clase
    getattr(self, MemoryTypes.ATTRIBUTES).reset()

# Semantic cuve for resulting types of operations
class SemanticCube:
  def __init__(self):
    sum_operations = [
      [ Types.INT,  Types.FLT, None,      None,         None ],
      [ Types.FLT,  Types.FLT, None,      None,         None ],
      [ None,       None,      Types.STR, None,         None ],
      [ None,       None,      None,      None,         None ],
      [ None,       None,      None,      None,         None ]
    ]
    minus_multiply_divide_operations = [
      [ Types.INT,  Types.FLT, None,      None,         None ],
      [ Types.FLT,  Types.FLT, None,      None,         None ],
      [ None,       None,      None,      None,         None ],
      [ None,       None,      None,      None,         None ],
      [ None,       None,      None,      None,         None ]
    ]
    # relational: >, <, >=, <=, gt, lt, gte,lte
    relational_operations_one = [
      [ Types.BOOL, Types.BOOL, None,      None,        None ],
      [ Types.BOOL, Types.BOOL, None,      None,        None ],
      [ None,       None,       None,      None,        None ],
      [ None,       None,       None,      None,        None ],
      [ None,       None,       None,      None,        None ]
    ]
    # relational: ==, ~=, eq, neq
    relational_operations_two = [
      [ Types.BOOL, Types.BOOL, None,       None,       None ],
      [ Types.BOOL, Types.BOOL, None,       None,       None ],
      [ None,       None,       Types.BOOL, None,       None ],
      [ None,       None,       None,       Types.BOOL, None ],
      [ None,       None,       None,       None,       None ]
    ]
    logical_operations = [
      [ None,       None,       None,       None,       None ],
      [ None,       None,       None,       None,       None ],
      [ None,       None,       None,       None,       None ],
      [ None,       None,       None,       Types.BOOL, None ],
      [ None,       None,       None,       None,       None ]
    ]
    # ~, not
    not_operations = [ None, None, None, Types.BOOL, None ]
    # +, - (as positive and negative)
    unary_arithmetic_operations = [ Types.INT, Types.FLT, None, None, None ]

    self._semantic_cube = [sum_operations,
                           minus_multiply_divide_operations,
                           relational_operations_one,
                           relational_operations_two,
                           logical_operations,
                           not_operations,
                           unary_arithmetic_operations]

    # index for semantic cube for each operator
    self._operators_index = {
      Operators.PLUS      : 0,
      Operators.MINUS     : 1,
      Operators.MULTIPLY  : 1,
      Operators.DIVIDE    : 1,
      Operators.L_THAN    : 2,
      Operators.G_THAN    : 2,
      Operators.L_THAN_EQ : 2,
      Operators.G_THAN_EQ : 2,
      Operators.GT        : 2,
      Operators.LT        : 2,
      Operators.GTE       : 2,
      Operators.LTE       : 2,
      Operators.EQ_TO     : 3,
      Operators.NOT_EQ    : 3,
      Operators.EQ        : 3,
      Operators.NEQ       : 3,
      Operators.OR_OP     : 4,
      Operators.AND_OP    : 4,
      Operators.AND       : 4,
      Operators.OR        : 4,
      Operators.NOT_OP    : 5,
      Operators.NOT       : 5,
      QuadOperations.PLUS_UNARY : 6,
      QuadOperations.MINUS_UNARY : 6,
    }

    # index for each type in semantic cube matrices
    self._types_index = {
      Types.INT  : 0,
      Types.FLT  : 1,
      Types.STR  : 2,
      Types.BOOL : 3
    }

  # Returns resulting type for operator and operands
  def validate_type(self, operator, operand_left_type, operand_right_type = None):
    operator_index = self._operators_index[operator]
    operand_left_index = self._types_index.get(operand_left_type, 4)

    if operand_right_type == None:
      return self._semantic_cube[operator_index][operand_left_index]

    operand_right_index = self._types_index.get(operand_right_type, 4)
    return self._semantic_cube[operator_index][operand_left_index][operand_right_index]

class SubCall:
  def __init__(self, sub_name, block_name):
    if block_name == None:
      block_name = Constants.GLOBAL_BLOCK
    self._sub_name = sub_name
    self._block_name = block_name
    self._param_count = 0
  
  def get_sub_name_block_name(self):
    return self._sub_name, self._block_name
  
  def get_param_count(self):
    return self._param_count
  
  def add_param_count(self):
    self._param_count += 1
  
  def get_sub_name(self):
    return self._sub_name

  def get_block_name(self):
    return self._block_name

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
    return getattr(self, type)[new_address]
  
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
  
  # attribute is an object of ConstantMemoryManager that comes from compilation
  # called only once
  def add_constant_memory(self, constant_memory):
    constants_map = constant_memory.get_map()
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
    elif memory_address >= MemoryRanges.LOCAL and memory_address <= MemoryRanges.LOCAL:
      type = MemoryTypes.LOCAL
    else:
      helpers.throw_error_no_line("Error in address")

    if type != MemoryTypes.LOCAL:
      upper_type = type.upper()
      new_address = memory_address - getattr(MemoryRanges, upper_type)
    # TODO: else

    return new_address, type

  def get_memory_value(self, memory_address):
    # TODO: add support for locals
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and getattr(self, type).is_pointer(new_address):
      stored_address = getattr(self, type).get_memory_value(new_address)
      return self.get_memory_value(stored_address)
    return getattr(self, type).get_memory_value(new_address)
  
  def set_memory_value(self, memory_address, value, assign_address = False):
    # TODO: add support for locals
    new_address, type = self.get_memory_address_type(memory_address)
    if type != MemoryTypes.CONSTANTS and getattr(self, type).is_pointer(new_address):
      if assign_address:
        getattr(self, type).set_address_to_pointer(new_address, value)
        return
      stored_address = getattr(self, type).get_memory_value(new_address)
      self.set_memory_value(stored_address, value)
      return
    getattr(self, type).set_memory_value(new_address, value)

  def get_memory_type(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_type(new_address)