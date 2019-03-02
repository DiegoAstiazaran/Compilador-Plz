# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens # Import tokens defined in lexer

# Define space and newline
space = " "
newline = "\n"

def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
  try:
    s = input('input > ')
  except EOFError:
    break
  if not s: continue
  result = parser.parse(s)
  print(result)