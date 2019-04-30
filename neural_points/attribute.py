from structures import OperandItem
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
  
  attribute_type, attribute_address, attribute_block, attribute_class = gv.function_directory.get_variable_item(attribute_name, Constants.GLOBAL_BLOCK, object_type)
  new_address = object_address[attribute_type] + attribute_address
  new_item = OperandItem(new_address, attribute_type, attribute_block, attribute_class) #
  gv.current_object = [object_type, attribute_name]
  
  gv.stack_operands.push(new_item)

def p_neural_restart_object(p):
  '''neural_restart_object :'''
  gv.current_object = None
