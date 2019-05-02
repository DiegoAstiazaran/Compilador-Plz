import operator

class Constants:
  # Name for global scope
  GLOBAL_BLOCK = 'global'

  # Name for class scope
  CLASS_BLOCK = 'class'

  # Name for constructor scope
  CONSTRUCTOR_BLOCK = 'constructor'

  FALSE_BOTTOM_IF_CONDITION = 'false_bottom_if_condition'

  FALSE_BOTTOM_EXPRESSION = 'false_bottom_expression'

  TRUE = 'True'
  FALSE = 'False'
  BOOLEAN = [TRUE, FALSE]

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
  unary = [NOT, NOT_OP]
  binary = relational + logical + plus_minus + multiply_divide

# Enum for quad operations
class QuadOperations:
  WRITE           = 'write'
  READ_ITEM       = 'read_item'
  READ_END        = 'read_end'
  READ_LN         = 'real_ln'
  WRITE_NEW_LINE  = 'write_new_line'
  WRITE_SPACE     = 'write_space'
  RETURN          = 'return'
  GOTO            = 'goto'
  GOTO_F          = 'goto_f'
  GOTO_T          = 'goto_t'
  ERA             = 'era'
  PARAM           = 'param'
  GOSUB           = 'gosub'
  PLUS_UNARY      = 'positive'
  MINUS_UNARY     = 'negative'
  VER             = 'ver'
  CHECK_DIV       = 'check_div'
  EQUAL_ADDRESS   = 'eq_address' 
  THIS_PARAM      = 'this_param'
  unary = [PLUS_UNARY, MINUS_UNARY]

class Defaults:
  INT = 0
  FLT = 0.0
  STR = ''
  BOOL = False

class MemoryTypes:
  GLOBAL     = "Global"
  LOCAL      = "Local"
  CONSTANTS  = "Constants"
  SCOPE      = "Scope"
  TEMPORAL   = "Temporal"
  ATTRIBUTES = "Attributes"
  POINTERS   = "Pointers"

class MemoryRanges:
  INT          = 0       # 0
  INT_SIZE     = 1000
  INT_MAX      = INT + INT_SIZE
  FLT          = INT_MAX # 1000
  FLT_SIZE     = 1000
  FLT_MAX      = FLT + FLT_SIZE
  STR          = FLT_MAX # 2000
  STR_SIZE     = 2000
  STR_MAX      = STR + STR_SIZE
  BOOL         = STR_MAX # 4000
  BOOL_SIZE    = 1000
  BOOL_MAX     = BOOL + BOOL_SIZE 
  TYPES_LIMIT  = BOOL_MAX # 5000

  SCOPE        = 0                       # 0
  SCOPE_MAX    = SCOPE + TYPES_LIMIT
  TEMPORAL     = SCOPE_MAX               # 5000
  TEMPORAL_MAX = TEMPORAL + TYPES_LIMIT
  POINTERS     = TEMPORAL + BOOL_MAX     # 10000 # Aqui no hay tipos
  POINTERS_SIZE = 1000
  POINTERS_MAX = POINTERS + POINTERS_SIZE # 11000
  
  CONSTANTS     = 0 # -> primitives
  CONSTANTS_MAX = CONSTANTS + TYPES_LIMIT
  GLOBAL        = 10000                   # 10000 # -> scope, temporal, pointers
  GLOBAL_MAX    = GLOBAL + POINTERS_MAX   # 21000
  LOCAL         = 30000                   # 30000 # -> scope, temporal, pointers
  LOCAL_MAX     = LOCAL + POINTERS_MAX    # 41000
  ATTRIBUTES    = 0 # -> primitives    # new map for each class
