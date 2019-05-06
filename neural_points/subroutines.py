from constants import Constants, Types, QuadOperations, MemoryTypes, Operators, MemoryRanges
from structures import Quad, OperandItem, SubCall
import global_variables as gv      # Import global variables
import helpers
from lexer import lexer

### Subroutine declaration

# Called after ID in subroutine declaration
def p_neural_sub_decl_id(p):
  '''neural_sub_decl_id :'''
  gv.memory_manager.reset_local()
  gv.current_block = p[-1]
  if gv.current_last_type == None:
    gv.current_last_type = Constants.CONSTRUCTOR_BLOCK
  gv.function_directory.add_block(gv.current_block, gv.current_last_type, gv.current_is_public, gv.current_class_block)
  if gv.current_last_type == Constants.CONSTRUCTOR_BLOCK:
    gv.current_last_type = gv.current_block
  gv.subroutine_directory.add_subroutine(gv.current_class_block, gv.current_block, gv.quad_list.next(), gv.current_is_public, gv.current_last_type)
  gv.current_last_type = None

  if gv.current_class_block is not None:
    for type in Types.primitives:
      memory_address = gv.memory_manager.get_memory_address(Types.INT, MemoryTypes.SCOPE, gv.current_block, gv.current_class_block)
      gv.function_directory.add_variable('this-' + type, gv.current_block, Types.INT, None, memory_address, gv.current_class_block)
      operand_item = OperandItem(memory_address, Types.INT)
      gv.subroutine_directory.add_param(gv.current_block, operand_item, gv.current_class_block)

def p_neural_param_decl(p):
  '''neural_param_decl :'''
  param = gv.stack_operands.pop()
  gv.subroutine_directory.add_param(gv.current_block, param, gv.current_class_block)

### Return

def p_neural_return_value(p):
  '''neural_return_value :'''
  gv.current_return_has_value = True

def p_neural_return_expression(p):
  '''neural_return_expression :'''
  if gv.current_block == Constants.GLOBAL_BLOCK:
    helpers.throw_error("Syntax error, return statement must be in subroutine")

  subroutine_type = gv.function_directory.get_sub_type(gv.current_block, gv.current_class_block)
  if subroutine_type == Constants.CONSTRUCTOR_BLOCK:
    helpers.throw_error("Invalid return statement in constructor")

  quad = Quad(QuadOperations.RETURN)

  if gv.current_return_has_value:
    expression = gv.stack_operands.pop()
    return_value_type = expression.get_type()
    quad.add_element(expression.get_value())
  else:
    return_value_type = Types.VOID

  if return_value_type != subroutine_type:
    if subroutine_type == Types.VOID:
      helpers.throw_error("Invalid return statement in void subroutine")
    else:
      if return_value_type == Types.VOID:
        helpers.throw_error("Return statement must have an expression")
      else:
        helpers.throw_error("Type mismatch in return value")

  gv.quad_list.add(quad)
  gv.current_return_has_value = False
  gv.current_sub_has_return_stmt = True

def p_neural_sub_end(p):
  '''neural_sub_end : '''
  subroutine_type = gv.function_directory.get_sub_type(gv.current_block, gv.current_class_block)
  if subroutine_type != Types.VOID and subroutine_type != Constants.CONSTRUCTOR_BLOCK and not gv.current_sub_has_return_stmt:
    helpers.throw_error("Subroutine must have return statement")
  if not gv.current_sub_has_return_stmt:
    quad = Quad(QuadOperations.RETURN)
    gv.quad_list.add(quad)
  gv.current_sub_has_return_stmt = False
  gv.function_directory.free_memory(gv.current_block, gv.current_class_block)
  gv.current_block = Constants.GLOBAL_BLOCK

### Subroutine calls

# keep the first id of a subcall in a global variable
def p_neural_sub_call_first_id(p):
  '''neural_sub_call_first_id :'''
  gv.sub_call_first_id = p[-1]

# keep the second id of a subcall in a global variable
def p_neural_sub_call_second_id(p):
  '''neural_sub_call_second_id :'''
  gv.sub_call_second_id = p[-1]

# subroutine has a return value, so it takes action to assign it or use it.
def p_neural_sub_call_return_value(p):
  '''neural_sub_call_return_value :'''
  helper_sub_call_end(True)

# subroutine does not hav a return value, so it cant be assigned or used as operation
def p_neural_sub_call_no_return_value(p):
  '''neural_sub_call_no_return_value :'''
  helper_sub_call_end(False)
 
# Checks whether an subroutine is a method or a subroutine, 
# checks if it exists in class, global scope or parent class. 
def p_neural_sub_call(p):
  '''neural_sub_call :'''
  if gv.sub_call_second_id is None: # It's not an object's subroutine
    subroutine_name = gv.sub_call_first_id
    if gv.current_this:
      call_class_name = gv.current_class_block
      object_name = None
    elif gv.current_class_block is not None and gv.subroutine_directory.subroutine_exists(subroutine_name, gv.current_class_block):
      call_class_name = gv.current_class_block
      object_name = None
    else:
      call_class_name = None
      object_name = None
  else: # It's an object $ subroutine
    subroutine_name = gv.sub_call_second_id
    object_name = gv.sub_call_first_id
    call_class_name = gv.function_directory.get_variable_type_deep(object_name, gv.current_block, gv.current_class_block)
  
  gv.sub_call_first_id = None
  gv.sub_call_second_id = None
  gv.current_this = False

  if not gv.subroutine_directory.subroutine_exists(subroutine_name, call_class_name):
    helpers.throw_error("Method " + subroutine_name + " doesn't exist.")
  
  # TODO: check this when inheritance is included
  if call_class_name is not None and gv.current_class_block != call_class_name and not gv.subroutine_directory.is_public(subroutine_name, call_class_name):
    helpers.throw_error("Method " + subroutine_name + " is not public and cannot be called in current location.")

  sub_call = SubCall(subroutine_name, call_class_name, object_name)

  if call_class_name is None:
    call_class_name = Constants.GLOBAL_BLOCK

  quad = Quad(QuadOperations.ERA, call_class_name, subroutine_name)

  subroutine_return_type = gv.subroutine_directory.get_type(subroutine_name, call_class_name)
  if subroutine_return_type != Types.VOID:
    memory_address = gv.memory_manager.get_memory_address(subroutine_return_type, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad.add_element(memory_address)
    sub_call.add_return_temporal_address(memory_address)

  gv.stack_sub_calls.push(sub_call)
  gv.quad_list.add(quad)

  # Passing current object memory_address as param
  if call_class_name != Constants.GLOBAL_BLOCK:
    if object_name is not None:
      memory_address = gv.function_directory.get_variable_address_deep(object_name, gv.current_block, gv.current_class_block)
      for type in Types.primitives:
        constant_address = gv.memory_manager.get_constant_memory_address(memory_address[type], Types.INT)
        quad = Quad(QuadOperations.THIS_PARAM, type, constant_address)
        gv.quad_list.add(quad)
    else:
      params_start = MemoryRanges.LOCAL + MemoryRanges.SCOPE + MemoryRanges.INT
      for index, type in enumerate(Types.primitives):
        quad = Quad(QuadOperations.THIS_PARAM, type, params_start + index)
        gv.quad_list.add(quad)
      
def p_neural_constructor_call(p):
  '''neural_constructor_call :'''
  if gv.current_block != Constants.GLOBAL_BLOCK:
    helpers.throw_error("Objects can only be declared in global scope")
  
  subroutine_name = p[-3]
  object_class_name = p[-3]
  object_name = p[-2]

  gv.function_directory.check_class_exists(object_class_name)
  
  sub_call = SubCall(subroutine_name, object_class_name, object_name)

  quad = Quad(QuadOperations.ERA, object_class_name, subroutine_name)

  gv.stack_sub_calls.push(sub_call)
  gv.quad_list.add(quad)

  id_item = gv.stack_operands.pop()
  memory_address = id_item.get_value()
  for type in Types.primitives:
    constant_address = gv.memory_manager.get_constant_memory_address(memory_address[type], Types.INT)
    quad = Quad(QuadOperations.THIS_PARAM, type, constant_address)
    gv.quad_list.add(quad)

# Validates that the amount and type of parameters matches with function 
# declaration and creates the PARAM quads
def p_neural_sub_call_arg(p):
  '''neural_sub_call_arg :'''
  arg = gv.stack_operands.pop()
  current_sub_call = gv.stack_sub_calls.top()
  param_count = current_sub_call.get_param_count()
  param_count = gv.subroutine_directory.fix_param_count(param_count, current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  if not gv.subroutine_directory.check_arg(arg.get_type(), param_count, current_sub_call.get_sub_name(), current_sub_call.get_block_name()):
    helpers.throw_error("Type mismatch in argument #{}, expected {}".format(param_count + 1, gv.subroutine_directory.get_param_type(param_count, current_sub_call.get_sub_name(), current_sub_call.get_block_name())) )
  
  quad = Quad(QuadOperations.PARAM, arg.get_value(), param_count)
  gv.quad_list.add(quad)

  param_count = gv.stack_sub_calls.top().add_param_count()

# validates the number of parameters and creates the GOSUB quad
def p_neural_sub_call_args_end(p):
  '''neural_sub_call_args_end :'''
  current_sub_call = gv.stack_sub_calls.top()
  # TODO: check what happens when extra params are sent
  if current_sub_call.get_param_count() != gv.subroutine_directory.get_param_count(current_sub_call.get_sub_name(), current_sub_call.get_block_name()):
    helpers.throw_error("Call not valid, less arguments than expected")
  
  quad = Quad(QuadOperations.GOSUB, current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  gv.quad_list.add(quad)

# checks if subroutine has return value or not, in case it was trying to be an assignment
def helper_sub_call_end(has_return_value):
  current_sub_call = gv.stack_sub_calls.pop()
  return_type = gv.subroutine_directory.get_type(current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  if has_return_value and return_type == Types.VOID:
    helpers.throw_error("Subcall does not have a return value.")
  if has_return_value:
    temporal = gv.memory_manager.get_memory_address(return_type, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    return_value = current_sub_call.get_return_temporal_address()
    quad = Quad(Operators.EQUAL, return_value, temporal)
    gv.quad_list.add(quad)
    temporal_operand = OperandItem(temporal, return_type)
    gv.stack_operands.push(temporal_operand)

# Check if id is an object, if not, thrown an error
def p_neural_check_id_is_object(p):
  '''neural_check_id_is_object :'''
  id_name = gv.sub_call_first_id
  id_type = gv.function_directory.get_variable_type_deep(id_name, gv.current_block, gv.current_class_block)
  if not gv.function_directory.is_class(id_type):
    helpers.throw_error(id_name + " is not an object")
