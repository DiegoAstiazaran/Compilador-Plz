from constants import Constants, Types, Operators, QuadOperations, MemoryTypes # Imports some constants
from structures import OperandItem, Quad, SubCall                 # Import OperandItem and Quad class
import global_variables as gv      # Import global variables
import helpers

from .expressions import add_to_operand_stack

#################################################
####### Function Directory Construction #########
#################################################

# Called when parsing starts and when subroutine ends
def p_neural_global_block(p):
  '''neural_global_block :'''
  # Set current block as global
  gv.current_block = Constants.GLOBAL_BLOCK

#
def p_neural_is_public_none(p):
  '''neural_is_public_none :'''
  gv.current_is_public = None

# Called after ID in every declaration or initialization
# It can be in decl_init, parameter declaration or attribute declaration
def p_neural_var_decl_id(p):
  '''neural_var_decl_id :'''
  if gv.current_last_type == None:
    # Second previous element in p will be stored; DICT or CLASS_NAME
    gv.current_last_type = p[-2]
  gv.current_last_id = p[-1]

  memory_address = gv.memory_manager.get_memory_address(gv.current_last_type, MemoryTypes.SCOPE, gv.current_block, gv.current_class_block)

  gv.function_directory.add_variable(gv.current_last_id, gv.current_block, gv.current_last_type, gv.current_is_public, memory_address, gv.current_class_block)

  if gv.current_last_type not in Types.primitives:
    class_variables_size = gv.function_directory.get_class_variables_memory_size(gv.current_last_type)
    for type, size in class_variables_size.items():
      memory_type = MemoryTypes.GLOBAL
      if gv.current_block != Constants.GLOBAL_BLOCK and gv.current_class_block == None: # check
        memory_type = MemoryTypes.LOCAL
      gv.memory_manager.increase_counter(type, memory_type, size)

  # Add operand to operand stack in case it is a initialization
  add_to_operand_stack(memory_address, gv.current_last_type)

  gv.current_param_type = gv.current_last_type
  gv.current_last_type = None

def p_neural_param_decl(p):
  '''neural_param_decl :'''
  param = gv.stack_operands.pop()
  gv.subroutine_directory.add_param(gv.current_block, param, gv.current_class_block)

# Called after each primitive type
def p_neural_decl_type(p):
  '''neural_decl_type :'''
  gv.current_last_type = p[-1]

def p_neural_array_decl(p):
  '''neural_array_decl :'''
  dimension_size = p[-2]
  gv.function_directory.add_dimension(gv.current_last_id, gv.current_block, dimension_size, gv.current_class_block)

def p_neural_array_decl_end(p):
  '''neural_array_decl_end :'''
  if gv.current_block == Constants.GLOBAL_BLOCK and gv.current_class_block == None:
    memory_type = MemoryTypes.GLOBAL
  elif gv.current_class_block != None:
    memory_type = MemoryTypes.ATTRIBUTES
  else:
    memory_type = MemoryTypes.LOCAL
  
  array_size = gv.function_directory.get_array_size(gv.current_last_id, gv.current_block, gv.current_class_block)
  var_type = gv.function_directory.get_variable_type(gv.current_last_id, gv.current_block, gv.current_class_block)
  gv.memory_manager.increase_counter(var_type, memory_type, array_size - 1)

def p_neural_id_calls_p_empty(p):
  '''neural_id_calls_p_empty :'''
  id_name = gv.sub_call_first_id
  id_type, id_name, id_block, id_class = gv.function_directory.get_variable_item_deep(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type, id_block, id_class)
  gv.sub_call_first_id = None
