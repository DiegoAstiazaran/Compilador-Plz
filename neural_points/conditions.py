from constants import Constants, QuadOperations, Types
from structures import Quad
import global_variables as gv
import helpers

# Called when if condition starts
def p_neural_condition_if(p):
  '''neural_condition_if :'''
  gv.stack_jumps.push(Constants.FALSE_BOTTOM_IF_CONDITION)

# Called after if condition expression
def p_neural_condition_new_quad(p):
  '''neural_condition_new_quad :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

# called when block in if condition ends
def p_neural_condition_end_block(p):
  '''neural_condition_end_block :'''
  quad = Quad(QuadOperations.GOTO)
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)
  gv.quad_list.add(quad)

# Called in elsif statements to fill gotof quads
def p_neural_condition_fill_quad(p):
  '''neural_condition_fill_quad :'''
  end_block_index = gv.stack_jumps.pop()
  quad_index = gv.stack_jumps.pop()
  next_quad_index = gv.quad_list.next()
  if not gv.current_condition_has_else and gv.condition_end:
    next_quad_index -= 1
  gv.quad_list.add_element_to_quad(quad_index, next_quad_index)
  gv.stack_jumps.push(end_block_index)

# Called when else token is read
def p_neural_condition_else(p):
  '''neural_condition_else :'''
  gv.current_condition_has_else = True

# Called when if condition ends
def p_neural_condition_end(p):
  '''neural_condition_end :'''
  gv.condition_end = True
  if not gv.current_condition_has_else:
    p_neural_condition_fill_quad(p)
  last_goto_index = gv.stack_jumps.top()
  if not gv.current_condition_has_else:
    gv.quad_list.erase(last_goto_index)
    gv.stack_jumps.pop()
  while gv.stack_jumps.top() != Constants.FALSE_BOTTOM_IF_CONDITION:
     quad_index = gv.stack_jumps.pop()
     gv.quad_list.add_element_to_quad(quad_index, gv.quad_list.next())
  gv.stack_jumps.pop()
  gv.condition_end = False
