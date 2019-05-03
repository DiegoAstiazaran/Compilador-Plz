from constants import Constants, MemoryRanges, Types, MemoryTypes, Operators, QuadOperations
from structures import OperandItem, Quad
import global_variables as gv      # Import global variables
import helpers

def p_neural_at_attribute(p):
  '''neural_at_attribute :'''
  object_pair = gv.stack_operands.pop()
  object_address = object_pair.get_value()
  object_name = gv.function_directory.get_var_name_from_address(object_address, gv.current_block, gv.current_class_block)
  object_type = object_pair.get_type()
  attribute_name = p[-1]

  if not gv.function_directory.is_class(object_type):
    helpers.throw_error(object_name + " is not an object")
  
  if not gv.function_directory.attribute_exists(attribute_name, object_type):
    helpers.throw_error("Attribute " + attribute_name + " doesn't exist.")

  if gv.current_class_block != object_type and not gv.function_directory.is_attribute_public(attribute_name, object_type):
    helpers.throw_error("Attribute " + attribute_name + " is not public and cannot be called in current location.")
  
  attribute_type, attribute_address, attribute_block, attribute_class = gv.function_directory.get_variable_item_deep(attribute_name, Constants.GLOBAL_BLOCK, object_type)
  new_address = object_address[attribute_type] + attribute_address
  new_item = OperandItem(new_address, attribute_type, attribute_block, attribute_class) #
  gv.current_object = [object_type, attribute_name]
  
  gv.stack_operands.push(new_item)

def p_neural_this(p):
  '''neural_this :'''
  gv.current_this = True

def p_neural_id_attr_access_end(p):
  '''neural_id_attr_access_end :'''
  operand_item = gv.stack_operands.pop()
  memory_address = operand_item.get_value()
  if operand_item.get_block_name() == Constants.GLOBAL_BLOCK and gv.function_directory.is_class(operand_item.get_class_name()):
    this_index = Types.primitives.index(operand_item.get_type())
    this_address = MemoryRanges.LOCAL + MemoryRanges.SCOPE + MemoryRanges.INT + this_index
    value_constant_address = gv.memory_manager.get_constant_memory_address(memory_address, Types.INT)
    temporal_int = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad = Quad(Operators.PLUS, value_constant_address, this_address, temporal_int)
    gv.quad_list.add(quad)
    temporal_pointer = gv.memory_manager.get_next_pointer(gv.current_block, gv.current_class_block)
    quad = Quad(QuadOperations.EQUAL_ADDRESS, temporal_int, temporal_pointer)
    gv.quad_list.add(quad)
    memory_address = temporal_pointer
  
  operand_item = OperandItem(memory_address, operand_item.get_type(), operand_item.get_block_name(), operand_item.get_class_name())
  gv.stack_operands.push(operand_item)

  gv.current_object = None
  gv.current_this = False
