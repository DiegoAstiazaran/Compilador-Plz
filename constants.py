import operator

class Constants:
  # Name for global scope
  GLOBAL_BLOCK = 'global'

  # Name for class scope
  CLASS_BLOCK = 'class'

  # Name for constructor scope
  CONSTRUCTOR_BLOCK = 'constructor'

  FALSE_BOTTOM_IF_CONDITION = 'false_bottom_if_condition'

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
  PLUS_UNARY      = 'positive'
  MINUS_UNARY     = 'negative'
  unary = [PLUS_UNARY, MINUS_UNARY]

class Defaults:
  INT = 0
  FLT = 0.0
  STR = ''
  BOOL = False

class MemoryTypes:
  CONSTANTS  = "Constants"
  SCOPE      = "Scope"
  TEMPORAL   = "Temporal"
  ATTRIBUTES = "Attributes"
  LOCAL      = "Local"
  GLOBAL     = "Global"

class MemoryRanges:
  INT       = 0
  FLT       = 1000
  STR       = 2000
  BOOL      = 4000
  BOOL_MAX  = 5000
  SCOPE_START      = 0
  TEMPORAL_START   = 5000
  ATTRIBUTES_START = 10000
  ATTRIBUTES_MAX   = 15000
  class Constants:
    START  = 0
    END    = 4999
    INT  = 0
    FLT  = 1000
    STR  = 2000
    BOOL = 4000
  class Global: # global y temporal
    START  = 5000
    END    = 14999
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
    START  = 15000
    END    = 29999
    class Scope:
      INT  = 15000
      FLT  = 16000
      STR  = 17000
      BOOL = 19000
    class Temporal:
      INT  = 20000
      FLT  = 21000
      STR  = 22000
      BOOL = 24000
    class Attributes:
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