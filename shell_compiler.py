from compiler import compiler
from input import get_input

input = get_input()
errors = compiler(input)
for error in errors:
  print (error)