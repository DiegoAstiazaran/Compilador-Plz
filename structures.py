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
      raise Exception("Quad operator must be different from None")
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

class SpecificMemoryMapManager:
  def __init__(self, first_class, second_class = None):
    if second_class is None:
      ranges = getattr(MemoryRanges, first_class)
    else:
      ranges = getattr(getattr(MemoryRanges, first_class), second_class)
    setattr(self, Types.INT, ranges.INT)
    setattr(self, Types.FLT, ranges.FLT)
    setattr(self, Types.STR, ranges.STR)
    setattr(self, Types.BOOL, ranges.BOOL)

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
  
  def reset(self):
    SpecificMemoryMapManager.__init__(self, self._first, self._second)

class ConstantMemoryManager(SpecificMemoryMapManager):
  def __init__(self):
    SpecificMemoryMapManager.__init__(self, MemoryTypes.CONSTANTS)
    self._memory = {type:{} for type in Types.primitives}

  def get_memory_address(self, value, type):
    if value in self._memory[type]:
      return self._memory[type][value]
    new_address = self.get_next(type)
    self._memory[type][value] = new_address
    return new_address
  
  def get_map(self):
    return self._memory

class ScopeMemoryMapManager:
  def __init__(self, type): # Global, Local
    self._scope_memory = SpecificMemoryMapManager(type, MemoryTypes.SCOPE)
    self._temporal_memory = SpecificMemoryMapManager(type, MemoryTypes.TEMPORAL)
    if type == MemoryTypes.LOCAL:
      self._attributes_memory = SpecificMemoryMapManager(type, MemoryTypes.ATTRIBUTES)

  def get_memory_map(self, memory_type):
    if memory_type == MemoryTypes.SCOPE:
      return self._scope_memory
    elif memory_type == MemoryTypes.TEMPORAL:
      return self._temporal_memory
    elif memory_type == MemoryTypes.ATTRIBUTES:
      return self._attributes_memory

class MemoryManager:
  def __init__(self):
    self._constant_memory_map = ConstantMemoryManager()
    self._global_memory_map = ScopeMemoryMapManager(MemoryTypes.GLOBAL)
    self._local_memory_map = ScopeMemoryMapManager(MemoryTypes.LOCAL)

  def get_memory_address(self, var_type, memory_type, current_block, current_class):
    if current_block == Constants.GLOBAL_BLOCK and current_class == None: # global
      return self._global_memory_map.get_memory_map(memory_type).get_next(var_type)
    elif current_block == None: # funcion
      return self._local_memory_map.get_memory_map(memory_type).get_next(var_type)
    else: # clase
      if current_block == None: # attribute
        return self._local_memory_map.get_memory_map(memory_type).get_next(var_type)
      else: # metodo
        return self._local_memory_map.get_memory_map(memory_type).get_next(var_type)
  
  def get_constant_memory_address(self, value, type):
    return self._constant_memory_map.get_memory_address(value, type)
  
  def get_last_global(self, type):
    return getattr(self._global_memory_map._scope_memory, type) - 1
  
  def reset_local(self): # para el local cada que empieces una funcion o metodo
    self._local_memory_map.get_memory_map(MemoryTypes.SCOPE).reset()
    self._local_memory_map.get_memory_map(MemoryTypes.TEMPORAL).reset()
  
  def reset_class(self): # cuando declaras una clase
    self._local_memory_map.get_memory_map(MemoryTypes.ATTRIBUTES).reset()

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

class VirtualMachineMemoryMap:
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
    if memory_address >= MemoryRanges.INT and  memory_address < MemoryRanges.FLT: 
      type = Types.INT
    elif memory_address >= MemoryRanges.FLT and  memory_address < MemoryRanges.STR:
      type = Types.FLT
    elif memory_address >= MemoryRanges.STR and  memory_address < MemoryRanges.BOOL:
      type = Types.STR
    elif memory_address >= MemoryRanges.BOOL and  memory_address < MemoryRanges.BOOL_MAX:
      type = Types.BOOL
    
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

class VirtualMachineMemoryMapLocal:
  def __init__(self):
    setattr(self, MemoryTypes.SCOPE, VirtualMachineMemoryMap())
    setattr(self, MemoryTypes.TEMPORAL, VirtualMachineMemoryMap())
  
  def get_memory_address_type(self, memory_address):
    if memory_address >= MemoryRanges.SCOPE_START and  memory_address < MemoryRanges.TEMPORAL_START:
      type = MemoryTypes.SCOPE
    elif memory_address >= MemoryRanges.TEMPORAL_START and  memory_address < MemoryRanges.ATTRIBUTES_START:
      type = MemoryTypes.TEMPORAL
    elif memory_address >= MemoryRanges.ATTRIBUTES_START and  memory_address < MemoryRanges.ATTRIBUTES_MAX:
      type = MemoryTypes.ATTRIBUTES
    
    upper_type = (type + '_start').upper()
    new_address = memory_address - getattr(MemoryRanges, upper_type)
    return new_address, type
  
  def get_memory_value(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_value(new_address)
  
  def set_memory_value(self, memory_address, value):
    new_address, type = self.get_memory_address_type(memory_address)
    getattr(self, type).set_memory_value(new_address, value)
  
  def get_memory_type(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_type(new_address)

class VirtualMachineMemoryMapManager:
  def __init__(self):
    setattr(self, MemoryTypes.GLOBAL, VirtualMachineMemoryMapLocal())
    setattr(self, MemoryTypes.CONSTANTS, VirtualMachineMemoryMapLocal())
    self._execution_stack = Stack()
  
  def add_constant_memory(self, constant_memory):
    constants_map = constant_memory.get_map()
    for type, type_map in constants_map.items():
      for key, value in type_map.items():
        new_address = value - MemoryRanges.Constants.START
        if type ==  Types.BOOL:
          key = bool(key)
        getattr(self, MemoryTypes.CONSTANTS).set_memory_value(new_address, key)

  def get_memory_address_type(self, memory_address):
    if memory_address >= MemoryRanges.Global.START and memory_address <= MemoryRanges.Global.END:
      type = MemoryTypes.GLOBAL
    elif memory_address >= MemoryRanges.Constants.START and memory_address <= MemoryRanges.Constants.END:
      type = MemoryTypes.CONSTANTS

    new_address = memory_address - getattr(MemoryRanges, type).START
    return new_address, type

  def get_memory_value(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_value(new_address)
  
  def set_memory_value(self, memory_address, value):
    new_address, type = self.get_memory_address_type(memory_address)
    getattr(self, type).set_memory_value(new_address, value)

  def get_memory_type(self, memory_address):
    new_address, type = self.get_memory_address_type(memory_address)
    return getattr(self, type).get_memory_type(new_address)