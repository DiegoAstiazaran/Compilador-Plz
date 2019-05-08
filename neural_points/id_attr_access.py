from constants import Constants, MemoryRanges, MemoryTypes, Operators, QuadOperations, Types 
from structures import OperandItem, Quad
import global_variables as gv      # Import global variables
import helpers

from .expressions import add_to_operand_stack

### This operator

def p_neural_this(p):
  '''neural_this :'''
  if gv.current_class_block is None:
    helpers.throw_error("Can't use this keyword outside of class subroutine.")
  gv.current_this = True

def p_neural_create_pointer(p):
  '''neural_create_pointer :'''
  array_item = gv.stack_operands.pop()
  array_address = array_item.get_value()
  array_type = array_item.get_type()
  block_name = array_item.get_block_name()
  class_name = array_item.get_class_name()

  if type(array_address) is not int:
    helpers.throw_error("Syntax error in input!")
  
  if array_item.is_list():
    helpers.throw_error("Incorrect operation with list.")

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
  operand_item.set_is_list(array_item.is_list())
  gv.stack_operands.push(operand_item)

### Object attribute

def p_neural_at_attribute(p):
  '''neural_at_attribute :'''
  object_item = gv.stack_operands.pop()
  object_address = object_item.get_value()
  # TODO: checar la func que obtiene nombre si no esta en scope
  object_name = gv.function_directory.get_var_name_from_address(object_address, gv.current_block, gv.current_class_block)
  object_type = object_item.get_type()
  attribute_name = p[-1]

  if not gv.function_directory.is_class(object_type):
    helpers.throw_error(object_name + " is not an object")
  
  if not gv.function_directory.attribute_exists(attribute_name, object_type):
    helpers.throw_error("Attribute " + attribute_name + " doesn't exist.")

  if gv.current_class_block != object_type and not gv.function_directory.is_attribute_public(attribute_name, object_type):
    helpers.throw_error("Attribute " + attribute_name + " is not public and cannot be called in current location.")
  
  attribute_type, attribute_address, attribute_block, attribute_class = gv.function_directory.get_variable_item_deep(attribute_name, Constants.GLOBAL_BLOCK, object_type)
  new_item = OperandItem(attribute_address, attribute_type, attribute_block, attribute_class)
  new_item.set_object_reference(object_address[attribute_type])
  
  gv.stack_operands.push(new_item)

### Array access

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

def p_neural_id_attr_access_end(p):
  '''neural_id_attr_access_end :'''
  operand_item = gv.stack_operands.pop()
  memory_address = operand_item.get_value()
  if operand_item.has_pending_object_reference() or operand_item.get_object_reference() is not None:
    if operand_item.has_pending_object_reference(): # this is in param
      this_index = Types.primitives.index(operand_item.get_type())
      object_reference_variable = MemoryRanges.LOCAL + MemoryRanges.SCOPE + MemoryRanges.INT + this_index
      temporal = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
      quad = Quad(QuadOperations.WRITE_ADDRESS, object_reference_variable, temporal)
      gv.quad_list.add(quad)
      object_reference_address = temporal

    else: # object reference is stored in operand_item
      object_reference = operand_item.get_object_reference()
      object_reference_address = gv.memory_manager.get_constant_memory_address(object_reference, Types.INT)

    temporal = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad = Quad(QuadOperations.READ_ADDRESS, memory_address, temporal)
    gv.quad_list.add(quad)

    temporal_2 = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad = Quad(Operators.PLUS, object_reference_address, temporal, temporal_2)
    gv.quad_list.add(quad)

    temporal_pointer = gv.memory_manager.get_next_pointer(gv.current_block, gv.current_class_block)
    quad = Quad(QuadOperations.WRITE_ADDRESS, temporal_2, temporal_pointer)
    gv.quad_list.add(quad)
    memory_address = temporal_pointer
  
  is_list = operand_item.is_list()
  operand_item = OperandItem(memory_address, operand_item.get_type(), operand_item.get_block_name(), operand_item.get_class_name())
  operand_item.set_is_list(is_list)
  gv.stack_operands.push(operand_item)

  gv.current_this = False