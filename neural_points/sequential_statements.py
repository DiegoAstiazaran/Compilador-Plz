from constants import QuadOperations, Types
from structures import Quad
import global_variables as gv      # Import global variables
import helpers

### Write

def p_neural_print_new_line(p):
  '''neural_print_new_line :'''
  gv.print_new_line = True

def p_neural_print_no_new_line(p):
  '''neural_print_no_new_line :'''
  gv.print_new_line = False

# Called after every expression to be printed
def p_neural_write_expression(p):
  '''neural_write_expression :'''
  expression = gv.stack_operands.pop()
  quad = Quad(QuadOperations.WRITE, expression.get_value())
  gv.quad_list.add(quad)

# Called after every print statement
def p_neural_write_end(p):
  '''neural_write_end :'''
  if not gv.print_new_line:
    return
  quad = Quad(QuadOperations.WRITE_NEW_LINE)
  gv.quad_list.add(quad)

# Called after every comma in print statements
def p_neural_write_space(p):
  '''neural_write_space :'''
  quad = Quad(QuadOperations.WRITE_SPACE)
  gv.quad_list.add(quad)

### Read

# Called after each item to be read in a read statement
# Reads item for item in the read statement
def p_neural_read_item(p):
  '''neural_read_item :'''
  read_item = gv.stack_operands.pop()
  read_item_helper(read_item, QuadOperations.READ_ITEM)

# Called after read line statement
# Reads entire line using quad operation READ_LN
def p_neural_read_ln(p):
  '''neural_read_ln :'''
  read_item = gv.stack_operands.pop()
  read_item_helper(read_item, QuadOperations.READ_LN)

# Called at the end of read statement
# Reads end line of a read statement.
def p_neural_read_end(p):
  '''neural_read_end :'''
  quad = Quad(QuadOperations.READ_END)
  gv.quad_list.add(quad)

# Used to create quad for item to be read
def read_item_helper(read_item, quad_operation):
  if read_item.get_type() not in Types.primitives:
    helpers.throw_error("Cannot assign input")
  quad = Quad(quad_operation, read_item.get_value())
  gv.quad_list.add(quad)