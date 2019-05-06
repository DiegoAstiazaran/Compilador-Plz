from constants import QuadOperations, Types, Constants, MemoryTypes, Operators, MemoryRanges
from structures import Quad, OperandItem
import global_variables as gv      # Import global variables
import helpers
from lexer import lexer

from .expressions import add_to_operand_stack
from .attribute import p_neural_at_attribute

# solves expression for array or first part of matrix
def p_neural_array_access_first(p):
  '''neural_array_access_first :'''
  array_access(0)

# Solves expression for second part of matrix
def p_neural_array_access_second(p):
  '''neural_array_access_second :'''
  array_access(1)

def array_access(index):
  value = gv.stack_operands.pop()
  if value.get_type() != Types.INT:
    helpers.throw_error("Expression to access array must resolve as an integer.")
  array_item = gv.stack_operands.top()
  array_address = array_item.get_value()
  array_block = array_item.get_block_name()
  array_class = array_item.get_class_name()

  dimension_size = gv.function_directory.get_variable_dimension( \
    array_address, array_block, index, array_class)

  if dimension_size is None:
    helpers.throw_error("Can't perform such array operation")
  quad = Quad(QuadOperations.VER, value.get_value(), dimension_size)
  gv.quad_list.add(quad)
  gv.array_access_indices.append(value.get_value())

def p_neural_array_access_end(p):
  '''neural_array_access_end :'''
  array_item = gv.stack_operands.pop()
  indices = gv.array_access_indices
  gv.array_access_indices = []
  array_address = array_item.get_value()
  array_type = array_item.get_type()
  block_name = array_item.get_block_name()
  class_name = array_item.get_class_name()

  array_dimension_count = gv.function_directory.get_array_dimensions_count(array_address, block_name, class_name)
  if len(indices) != array_dimension_count:
    helpers.throw_error("Can't perform such array operation")

  temporal = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
  array_address_constant_address = gv.memory_manager.get_constant_memory_address(array_address, Types.INT)
  quad = Quad(Operators.PLUS, indices[-1], array_address_constant_address, temporal)
  gv.quad_list.add(quad)

  if len(indices) == 2:
    second_dimension = gv.function_directory.get_variable_dimension(array_address, gv.current_block, 1, gv.current_class_block)
    second_dimension_constant_address = gv.memory_manager.get_constant_memory_address(second_dimension, Types.INT)
    temporal_mult_result = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad = Quad(Operators.MULTIPLY, indices[0], second_dimension_constant_address, temporal_mult_result) ###
    gv.quad_list.add(quad)
    new_temporal = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad = Quad(Operators.PLUS, temporal, temporal_mult_result, new_temporal)
    gv.quad_list.add(quad)
    temporal = new_temporal
  
  pointer = gv.memory_manager.get_next_pointer(gv.current_block, gv.current_class_block)
  quad = Quad(QuadOperations.WRITE_ADDRESS, temporal, pointer)
  gv.quad_list.add(quad)
  operand_item = OperandItem(pointer, array_type, block_name, class_name)
  operand_item.set_object_reference(array_item.get_object_reference())
  operand_item.set_pending_object_reference(array_item.has_pending_object_reference())
  gv.stack_operands.push(operand_item)


def p_neural_create_pointer(p):
  '''neural_create_pointer :'''
  array_item = gv.stack_operands.pop()
  array_address = array_item.get_value()
  array_type = array_item.get_type()
  block_name = array_item.get_block_name()
  class_name = array_item.get_class_name()

  if block_name == Constants.GLOBAL_BLOCK and gv.function_directory.is_class(class_name):
    array_dimension_count = gv.function_directory.get_array_dimensions_count_(array_address, array_type, block_name, class_name)
  else:
    array_dimension_count = gv.function_directory.get_array_dimensions_count(array_address, block_name, class_name)
  
  if array_dimension_count > 0:
    helpers.throw_error("Can't use array without index.")

  pointer = gv.memory_manager.get_next_pointer(gv.current_block, gv.current_class_block)
  array_address_constant_address = gv.memory_manager.get_constant_memory_address(array_address, Types.INT)
  quad = Quad(QuadOperations.WRITE_ADDRESS, array_address_constant_address, pointer)
  gv.quad_list.add(quad)
  operand_item = OperandItem(pointer, array_type, block_name, class_name)
  operand_item.set_object_reference(array_item.get_object_reference())
  operand_item.set_pending_object_reference(array_item.has_pending_object_reference())
  gv.stack_operands.push(operand_item)

