from constants import QuadOperations, Types
from structures import Quad
import global_variables as gv      # Import global variables
import helpers

### Write

# Called after every expression to be printed
def p_neural_write_expression(p):
  '''neural_write_expression :'''
  expression = gv.stack_operands.pop()
  quad = Quad(QuadOperations.WRITE, expression.get_value())
  gv.quad_list.add(quad)

# Called after every print statement
def p_neural_write_new_line(p):
  '''neural_write_new_line :'''
  quad = Quad(QuadOperations.WRITE_NEW_LINE)
  gv.quad_list.add(quad)

# Called after every comma in print statements
def p_neural_write_space(p):
  '''neural_write_space :'''
  quad = Quad(QuadOperations.WRITE_SPACE)
  gv.quad_list.add(quad)

### Read

def p_neural_read(p):
  '''neural_read_stmt :'''
  read_item = gv.stack_operands.pop()
  if read_item.get_type() not in Types.primitives:
    helpers.throw_error("Cannot assign input")
  quad = Quad(QuadOperations.READ, read_item.get_value())
  gv.quad_list.add(quad)

