from constants import QuadOperations, Types, Operators
from structures import Quad
import global_variables as gv
import helpers

from .expressions import add_to_operand_stack

### When

# Called at the beggining of when cycle
# Pushes the quad the cycle will return to when the iteration is done
def p_neural_when_before_expression(p):
  '''neural_when_before_expression :'''
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)

# Called after repeat token in when cycle
# Validates that the expression is boolean and creates the GOTOF quad
def p_neural_when_repeat(p):
  '''neural_when_repeat :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

# Called at the end of when cycle
# Creates the GOTO quad to return to the beginning of the cycle
def p_neural_when_end(p):
  '''neural_when_end :'''
  goto_f_index = gv.stack_jumps.pop()
  goto_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO, goto_index)
  gv.quad_list.add(quad)
  next_index = gv.quad_list.next()
  gv.quad_list.add_element_to_quad(goto_f_index, next_index)

### Repeat

# Called at the beggining of repeat cycle
# Pushes the quad the cycle will return to after each iteration
def p_neural_repeat_start(p):
  '''neural_repeat_start :'''
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)

# Called at the end of repeat cycle
# Validates the expression is boolean and creates the GOTO_T quad
def p_neural_repeat_end(p):
  '''neural_repeat_end :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
      helpers.throw_error("Condition must be boolean")
  goto_t_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO_T, condition.get_value(), goto_t_index)
  gv.quad_list.add(quad)

### For

# Called after id token in for cycle
# Checks that the id is an integer or float and adds it to the stack.
def p_neural_for_id(p):
  '''neural_for_id :'''
  id_name = p[-1]
  id_type, id_name, id_block, id_class = gv.function_directory.get_variable_item_deep(id_name, gv.current_block, gv.current_class_block)
  if id_type != Types.INT and id_type != Types.FLT:
    helpers.throw_error("Variable must be integer or float")
  add_to_operand_stack(id_name, id_type, id_block, id_class)

# Called after assignment value
# Assigns the value to the variable that will be used in the cycle
def p_neural_for_assignment(p):
  '''neural_for_assignment :'''
  value_to_assign = gv.stack_operands.pop()
  id = gv.stack_operands.top()
  quad = Quad(Operators.EQUAL, value_to_assign.get_value(), id.get_value())
  gv.quad_list.add(quad)

# Called before expression in for cycle
# Checks the operator that will affect the iterating variable each iteration, 
# it may be plus, minus, multiplication or division.
def p_neural_for_before_expression(p):
  '''neural_for_before_expression :'''
  operator = Operators.PLUS if gv.stack_operators.empty() else gv.stack_operators.pop()
  gv.stack_for_operators.push(operator)
  gv.stack_jumps.push(gv.quad_list.next())

# Called after expression in for cycle
# Checks that the expression is boolean and creates the GOTO_F of the cycle. 
def p_neural_for_after_expression(p):
  '''neural_for_after_expression :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

# Called at the end of for cycle
# Fills all the GOTOS and changes the value of the 
# iterating value by its respective operation and value.
def p_neural_for_end(p):
  '''neural_for_end :'''
  change_value = gv.stack_operands.pop()
  id = gv.stack_operands.pop()
  operator = gv.stack_for_operators.pop()
  quad = Quad(operator, id.get_value(), change_value.get_value(), id.get_value())
  gv.quad_list.add(quad)

  goto_f_index = gv.stack_jumps.pop()
  goto_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO, goto_index)
  gv.quad_list.add(quad)
  next_index = gv.quad_list.next()
  gv.quad_list.add_element_to_quad(goto_f_index, next_index)
