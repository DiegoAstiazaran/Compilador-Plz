from constants import Constants, MemoryRanges, Types, MemoryTypes, Operators, QuadOperations
from structures import OperandItem, Quad
import global_variables as gv      # Import global variables
import helpers
from lexer import lexer

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

def p_neural_this(p):
  '''neural_this :'''
  if gv.current_class_block is None:
    helpers.throw_error("Can't use this keyword outside of class subroutine.")
  gv.current_this = True

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
  
  operand_item = OperandItem(memory_address, operand_item.get_type(), operand_item.get_block_name(), operand_item.get_class_name())
  gv.stack_operands.push(operand_item)

  gv.current_this = False
