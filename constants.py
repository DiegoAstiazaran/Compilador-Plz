class Constants:
  # Name for global scope
  GLOBAL_BLOCK = 'global'

  # Name for class scope
  CLASS_BLOCK = 'class'

  # Name for constructor scope
  CONSTRUCTOR_BLOCK = 'constructor'

  FALSE_BOTTOM_IF_CONDITION = 'false_bottom_if_condition'
  
# Enum for types
class Types:
  INT   = 'int'
  FLT   = 'flt'
  STR   = 'str'
  BOOL  = 'bool'
  VOID  = 'void'

  primitives = [INT, FLT, STR, BOOL]

# Enum for operators
class Operators:
  NOT_OP       = '~'
  NOT          = 'not'
  EQUAL        = '='
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

# Enum for quad operations
class QuadOperations:
  WRITE           = 'write'
  READ            = 'read'
  WRITE_NEW_LINE  = 'write_new_line'
  WRITE_SPACE     = 'write_space'
  RETURN          = 'return'
  GOTO            = 'goto'
  GOTO_F          = 'goto_f'
  GOTO_T          = 'goto_t'
  ERA             = 'era'
  PARAM           = 'param'
  GOSUB           = 'gosub'
