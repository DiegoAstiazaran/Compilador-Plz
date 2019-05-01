from constants import QuadOperations, Types, Constants, MemoryTypes, Operators
from structures import Quad, OperandItem
import global_variables as gv      # Import global variables
import helpers

from .expressions import add_to_operand_stack
from .attribute import p_neural_at_attribute

def p_neural_array_access_first(p):
  '''neural_array_access_first :'''
  array_access(0)

def p_neural_array_access_second(p):
  '''neural_array_access_second :'''
  array_access(1)

def array_access(index):
  value = gv.stack_operands.pop()
  if value.get_type() != Types.INT:
    helpers.throw_error("Expression to access array must resolve as an integer.")
  array_pair = gv.stack_operands.top()

  if gv.current_object is None:
    block = gv.current_block
    class_block = gv.current_class_block
    array_address = array_pair.get_value()
  else:
    block = Constants.GLOBAL_BLOCK
    class_block = gv.current_object[0]
    array_address = gv.current_object[1]

  dimension_size = gv.function_directory.get_variable_dimension(array_address, block, index, class_block)
  if dimension_size is None:
    helpers.throw_error("Can't perform such array operation")
  quad = Quad(QuadOperations.VER, value.get_value(), dimension_size)
  gv.quad_list.add(quad)
  gv.array_access_indices.append(value.get_value())

def p_neural_add_subcall_first_id_to_stack(p):
  '''neural_add_subcall_first_id_to_stack :'''
  id_name = gv.sub_call_first_id
  gv.sub_call_first_id = None
  id_type, id_name, id_block, id_class = gv.function_directory.get_variable_item(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type, id_block, id_class)

def p_neural_array_access_end(p):
  '''neural_array_access_end :'''
  array_item = gv.stack_operands.pop()
  indices = gv.array_access_indices
  gv.array_access_indices = []
  array_address = array_item.get_value()
  array_type = array_item.get_type()
  block_name = array_item.get_block_name()
  class_name = array_item.get_class_name()

  if gv.current_object is not None:
    array_address = gv.current_object[1]

  array_dimension_count = gv.function_directory.get_array_dimensions_count(array_address, block_name, class_name)
  if len(indices) != array_dimension_count:
    helpers.throw_error("Can't perform such array operation")
  memory_type = MemoryTypes.GLOBAL
  # TODO: checar otro if como estos y quitar la segunda condicion 
  if gv.current_block != Constants.GLOBAL_BLOCK:
    memory_type = MemoryTypes.LOCAL
  temporal = gv.memory_manager.get_next_temporal(Types.INT, memory_type)
  array_address_constant_address = gv.memory_manager.get_constant_memory_address(array_address, Types.INT)
  quad = Quad(Operators.PLUS, indices[-1], array_address_constant_address, temporal) ####
  gv.quad_list.add(quad)
  if len(indices) == 2:
    second_dimension = gv.function_directory.get_variable_dimension(array_address, gv.current_block, 1, gv.current_class_block)
    second_dimension_constant_address = gv.memory_manager.get_constant_memory_address(second_dimension, Types.INT)
    temporal_mult_result = gv.memory_manager.get_next_temporal(Types.INT, memory_type)
    quad = Quad(Operators.MULTIPLY, indices[0], second_dimension_constant_address, temporal_mult_result) ###
    gv.quad_list.add(quad)
    new_temporal = gv.memory_manager.get_next_temporal(Types.INT, memory_type)
    quad = Quad(Operators.PLUS, temporal, temporal_mult_result, new_temporal)
    gv.quad_list.add(quad)
    temporal = new_temporal
  pointer = gv.memory_manager.get_next_pointer(memory_type)
  quad = Quad(QuadOperations.EQUAL_ADDRESS, temporal, pointer)
  gv.quad_list.add(quad)
  pair = OperandItem(pointer, array_type)
  gv.stack_operands.push(pair)
