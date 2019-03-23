# Enum for types
class Types:
  INT   = 'int'
  FLT   = 'flt'
  STR   = 'str'
  BOOL  = 'bool'

# Enum for operators
class Operators:
  NOT_OP       = '~'
  NOT          = 'not'
  PLUS         = '+'
  MINUS        = '-'
  MULTIPLY     = '*'
  DIVIDE       = '/'
  AND_OP       = '&'
  OR_OP        = '|'
  AND          = 'and'
  OR           = 'or'
  L_THAN       = '<'
  G_THAN       = '>'
  L_THAN_EQ    = '<='
  G_THAN_EQ    = '>='
  NOT_EQ       = '~='
  EQ_TO        = '=='
  LT           = 'lt'
  GT           = 'gt'
  LTE          = 'lte'
  GTE          = 'gte'
  NEQ          = 'neq'
  EQ           = 'eq'

  # Classification of operators
  relational = [L_THAN, G_THAN, L_THAN_EQ, G_THAN_EQ, NOT_EQ, EQ_TO,
                LT,     GT,     LTE,       GTE,       NEQ,    EQ ]
  logical = [AND_OP, OR_OP,
             AND,    OR   ]
  plus_minus = [PLUS, MINUS]
  multiply_divide = [MULTIPLY, DIVIDE]
  unary = [PLUS, MINUS, NOT, NOT_OP]
  unary_arithmetic = [PLUS, MINUS]

# Pair of operand value and type 
class OperandPair:
  def __init__(self, operand_value, operand_type):
    self._pair = (operand_value, operand_type)
  
  def __str__(self):
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

# Quad for intermediate code
class Quad:
  def __init__(self, instruction, first, second = None, third = None):
    if first is None and second is None and third is None:
      raise Exception("Quad must have at least two params different from None")
    self._quad = [instruction]
    if first is not None:
      self._quad.append(first)
    if second is not None:
      self._quad.append(second)
    if third is not None:
      self._quad.append(third)
  
  def __repr__(self):
    return ' '.join(str(i) for i in filter(None.__ne__, self._quad))

# Temporal memory manager
class TemporalMemory:
  def __init__(self):
    self._next_available = 0
  
  def get_available(self):
    self._next_available += 1
    return 'temp_%d' % (self._next_available - 1)

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
      [ None,       Types.BOOL, None,      None,        None ],
      [ None,       None,       None,      None,        None ],
      [ None,       None,       None,      None,        None ],
      [ None,       None,       None,      None,        None ]
    ]
    # relational: ==, ~=, eq, neq
    relational_operations_two = [ 
      [ Types.BOOL, Types.BOOL, None,       None,       None ],
      [ None,       Types.BOOL, None,       None,       None ],
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
      "unary_arithmetic"  : 6,
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
      if operator in Operators.unary_arithmetic:
          operator_index = self._operators_index["unary_arithmetic"]
      return self._semantic_cube[operator_index][operand_left_index]

    operand_right_index = self._types_index.get(operand_right_type, 4)
    return self._semantic_cube[operator_index][operand_left_index][operand_right_index]