import itertools

from constants import MemoryTypes, Operators, Types
from structures import OperandItem, Quad
import global_variables as gv      # Import global variables
import helpers

from .expressions import add_to_operand_stack

# Called after ID in every declaration or initialization
# It can be in decl_init, parameter declaration or attribute declaration
def p_neural_var_decl_id(p):
  '''neural_var_decl_id :'''
  if gv.current_last_type == None:
    # Second previous element in p will be stored; CLASS_NAME
    gv.current_last_type = p[-2]
  gv.current_last_id = p[-1]

  # if it is an object counters will not be modified, only next is returned as reference for start
  memory_address = gv.memory_manager.get_memory_address(gv.current_last_type, MemoryTypes.SCOPE, gv.current_block, gv.current_class_block)

  gv.function_directory.add_variable(gv.current_last_id, gv.current_block, gv.current_last_type, gv.current_is_public, memory_address, gv.current_class_block)

  # When declaring an object
  if gv.current_last_type not in Types.primitives:
    class_variables_size = gv.function_directory.get_class_variables_memory_size(gv.current_last_type)
    for type, size in class_variables_size.items():
      gv.memory_manager.increase_counter(type, size, gv.current_block, gv.current_class_block)

  # Add operand to operand stack in case it is an initialization
  add_to_operand_stack(memory_address, gv.current_last_type)

  gv.current_param_type = gv.current_last_type
  gv.current_last_type = None

# Called after each primitive type
# Gets the last type of a variable
def p_neural_decl_type(p):
  '''neural_decl_type :'''
  gv.current_last_type = p[-1]

# Called after array size is specified in variable declaration
def p_neural_array_decl(p):
  '''neural_array_decl :'''
  dimension_size = p[-2]
  gv.function_directory.add_dimension(gv.current_last_id, gv.current_block, dimension_size, gv.current_class_block)

# Called after specifing sizes of array in declaration
def p_neural_array_decl_end(p):
  '''neural_array_decl_end :''' 
  array_size = gv.function_directory.get_array_size(gv.current_last_id, gv.current_block, gv.current_class_block)
  var_type = gv.stack_operands.top().get_type()
  gv.memory_manager.increase_counter(var_type, array_size - 1, gv.current_block, gv.current_class_block)

def p_neural_array_init_list(p):
  '''neural_array_init_list :'''
  gv.array_init_values = []

def p_neural_array_init_single_value(p):
  '''neural_array_init_single_value :'''
  value = gv.stack_operands.pop()
  gv.array_init_values = value

def p_neural_array_init_value(p):
  '''neural_array_init_value :'''
  value = gv.stack_operands.pop()
  if len(gv.array_init_values) == 0 or type(gv.array_init_values[0]) is not list:
    gv.array_init_values.append(value)
  else:
    gv.array_init_values[-1].append(value)

def p_neural_matrix_init_array(p):
  '''neural_matrix_init_array :'''
  gv.array_init_values.append([])
    
def p_neural_array_init_end(p):
  '''neural_array_init_end :'''
  array_item = gv.stack_operands.top()
  array_type = array_item.get_type()
  array_address = array_item.get_value()
  dimensions_count = gv.function_directory.get_array_dimensions_count(array_address, gv.current_block, gv.current_class_block)
  first_dimension_size = gv.function_directory.get_variable_dimension(array_address, gv.current_block, 0, gv.current_class_block)
  if type(gv.array_init_values) is OperandItem:
    value = gv.array_init_values
    if value.get_type() != array_type:
      helpers.throw_error("Type mismatch in initialization.")
    array_size = gv.function_directory.get_array_size(array_address, gv.current_block, gv.current_class_block)
    for index in range(array_size):
      quad = Quad(Operators.EQUAL, value.get_value(), array_address + index)
      gv.quad_list.add(quad)
  else:
    if dimensions_count == 1:
      if len(gv.array_init_values) != first_dimension_size:
        helpers.throw_error("Amount of items in initialization does not match size.")
    else:
      second_dimension_size = gv.function_directory.get_variable_dimension(array_address, gv.current_block, 1, gv.current_class_block)
      if type(gv.array_init_values[0]) is list:
        arrays_sizes = list(map(len, gv.array_init_values))
        if len(set(arrays_sizes))!= 1 or \
          len(gv.array_init_values) != first_dimension_size or \
          len(gv.array_init_values[0]) != second_dimension_size:
          helpers.throw_error("Amount of items in initialization does not match size.")
        gv.array_init_values = list(itertools.chain.from_iterable(gv.array_init_values))
      else:
        if len(gv.array_init_values) != second_dimension_size:
          helpers.throw_error("Amount of items in initialization does not match size.")
        gv.array_init_values = gv.array_init_values * first_dimension_size

    for index, value in enumerate(gv.array_init_values):
      if value.get_type() != array_type:
        helpers.throw_error("Type mismatch in initialization.")
      quad = Quad(Operators.EQUAL, value.get_value(), array_address + index)
      gv.quad_list.add(quad)

  gv.array_init_values = None
