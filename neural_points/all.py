import global_variables as gv      # Import global variables
from lexer import lexer

from .expressions import add_to_operand_stack

def p_neural_id_calls_p_empty(p):
  '''neural_id_calls_p_empty :'''
  id_name = gv.sub_call_first_id
  id_type, id_name, id_block, id_class = gv.function_directory.get_variable_item_deep(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type, id_block, id_class)
  gv.sub_call_first_id = None
