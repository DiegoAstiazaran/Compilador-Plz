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

class MemoryTypes:
  CONSTANTS  = "Constants"
  SCOPE      = "Scope"
  TEMPORAL   = "Temporal"
  ATTRIBUTES = "Attributes"
  LOCAL      = "Local"
  GLOBAL     = "Global"

class MemoryRanges:
  class Constants:
    INT  = 0
    FLT  = 1000
    STR  = 2000
    BOOL = 4000
  class Global: # global y temporal
    class Scope:
      INT  = 5000
      FLT  = 6000
      STR  = 7000
      BOOL = 9000
    class Temporal:
      INT  = 10000
      FLT  = 11000
      STR  = 12000
      BOOL = 14000
  class Local:
    class Attributes:
      INT  = 15000
      FLT  = 16000
      STR  = 17000
      BOOL = 19000
    class Scope:
      INT  = 20000
      FLT  = 21000
      STR  = 22000
      BOOL = 24000
    class Temporal:
      INT  = 25000
      FLT  = 26000
      STR  = 27000
      BOOL = 29000

# class MemoryRanges:
#   class Constants:
#     INT  = 20000
#     FLT  = 20500
#     STR  = -10
#     BOOL = -10
#   class Global: # global y temporal
#     class Scope:
#       INT  = 5000
#       FLT  = 8000
#       STR  = -10
#       BOOL = -10
#     class Temporal:
#       INT  = 15000
#       FLT  = 17000
#       STR  = -10
#       BOOL = 19000
#   class Local: # local y temporal
#     class Attributes:
#       INT  = -10
#       FLT  = -10
#       STR  = -10
#       BOOL = -10
#     class Scope:
#       INT  = 11000
#       FLT  = 13000
#       STR  = -10
#       BOOL = -10
#     class Temporal:
#       INT  = 15000
#       FLT  = 17000
#       STR  = -10
#       BOOL = 19000