from lexer import lexer   # Import lexer
from constants import QuadOperations
from structures import Quad
import global_variables as gv

### Other

# Creates a goto before a block
def p_neural_new_goto(p):
  '''neural_new_goto :'''
  quad = Quad(QuadOperations.GOTO)
  quad_index = gv.quad_list.next()
  gv.quad_list.add(quad)
  gv.stack_jumps.push(quad_index)

# Fills goto previously created
def p_neural_fill_goto(p):
  '''neural_fill_goto :'''
  quad_index = gv.stack_jumps.pop()
  next_quad = gv.quad_list.next()
  gv.quad_list.add_element_to_quad(quad_index, next_quad)

# Use for debugging
# TODO: delete
def p_neural_new_line(p):
  '''neural_new_line :'''
  line = lexer.lineno
  if line not in gv.lines_read:
    print('Line #%d\n' % (line) )
  gv.lines_read.append(line)
