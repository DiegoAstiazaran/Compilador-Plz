# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.lex as lex # Import lex module

# Tokens for reserved words
reserved = {
  'return' : 'RETURN',
  'class' : 'CLASS',
  'under' : 'UNDER',
  'end' : 'END',
  'private' : 'PRIVATE',
  'public' : 'PUBLIC',
  'attributes' : 'ATTRIBUTES',
  'methods' : 'METHODS',
  'sub' : 'SUB',
  'void' : 'VOID',
  'if' : 'IF',
  'elsif' : 'ELSIF',
  'else' : 'ELSE',
  'while' : 'WHILE',
  'when' : 'WHEN',
  'repeat' : 'REPEAT',
  'for' : 'FOR',
  'from' : 'FROM',
  'by' : 'BY',
  'read' : 'READ',
  'read_ln' : 'READ_LN',
  'or' : 'OR',
  'and' : 'AND',
  'not' : 'NOT',
  'print' : 'PRINT',
  'int' : 'INT',
  'flt' : 'FLT',
  'bool' : 'BOOL',
  'str' : 'STR',
  'gt' : 'GT',
  'lt' : 'LT',
  'gte' : 'GTE',
  'lte' : 'LTE',
  'eq' : 'EQ',
  'neq' : 'NEQ',
  'True' : 'TRUE',
  'False' : 'FALSE',
  'this' : 'THIS'
}

# List of tokens that include reserved words tokens
tokens = [
  'ID',
  'CLASS_NAME',
	'COLON',
	'MONEY',
  'AT',
	'PLUS',
	'MINUS',
	'MULTIPLY',
	'DIVIDE',
	'L_PAREN',
	'R_PAREN',
	'DOT',
	'EQUAL',
	'L_BRACKET',
	'R_BRACKET',
  'COMMA',
  'L_THAN',
  'G_THAN',
  'NOT_EQ',
  'L_THAN_EQ',
  'G_THAN_EQ',
  'EQ_TO',
  'OR_OP',
  'AND_OP',
  'NOT_OP',
  'CTE_I',
  'CTE_F',
  'CTE_STR',
  'L_SQ_BRACKET',
  'R_SQ_BRACKET',
  'COMMENT',
  'MULTI_LINE_COMMENT',
] + list(reserved.values())

# Regular expressions for one character long tokens
t_COLON        = r':'
t_MONEY        = r'\$'
t_AT           = r'\@'
t_PLUS         = r'\+'
t_MINUS        = r'-'
t_MULTIPLY     = r'\*'
t_DIVIDE       = r'/'
t_L_PAREN      = r'\('
t_R_PAREN      = r'\)'
t_DOT          = r'\.'
t_EQUAL        = r'='
t_L_BRACKET    = r'{'
t_R_BRACKET    = r'}'
t_COMMA        = r','
t_L_THAN       = r'<'
t_G_THAN       = r'>'
t_NOT_EQ       = r'~='
t_L_THAN_EQ    = r'<='
t_G_THAN_EQ    = r'>='
t_EQ_TO        = r'=='
t_OR_OP        = r'\|'
t_AND_OP       = r'&'
t_NOT_OP       = r'~'
t_L_SQ_BRACKET = r'\['
t_R_SQ_BRACKET = r'\]'

# Functions with regex for complex tokens
def t_ID(t):
  r'[a-z][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'ID')
  return t

def t_CLASS_NAME(t):
  r'[A-Z][a-z]*'
  t.type = reserved.get(t.value,'CLASS_NAME')
  return t

def t_CTE_F(t):
  r'\d+\.\d+'
  t.value = float(t.value)
  return t

def t_CTE_I(t):
  r'\d+'
  t.value = int(t.value)
  return t

def t_CTE_STR(t):
  r'"[^"]*" | \'[^\']*\''
  t.value = t.value[1:-1]
  return t

def t_MULTI_LINE_COMMENT(t):
  r'\#\#\#(.|\n)*\#\#\#'
  t.lexer.lineno += t.value.count('\n')

def t_COMMENT(t):
  r'\#.*(\n|$)'
  t.lexer.lineno += 1

# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  t.lexer.skip(1)

# Initializes lexer
lexer = lex.lex()

# Code needed to test lexer
# while True:
#   try:
#     lexer = lex.lex()
#     # data = input('data > ')
#     file = input('Filename: ')
#     with open(file, 'r') as myfile:
#         s = myfile.read()
#     lexer.input(s)
#     while True:
#       tok = lexer.token()
#       if not tok:
#           break
#       print(tok)
#   except EOFError:
#     break
