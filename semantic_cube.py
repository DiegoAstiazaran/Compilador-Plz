from constants import Types, Operators, QuadOperations

# Semantic cube for resulting types of operations
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
