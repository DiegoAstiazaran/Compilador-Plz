from constants import Constants, MemoryRanges, MemoryTypes, Operators, QuadOperations, Types 
from structures import ListMethodCall, OperandItem, Quad, SubCall
import global_variables as gv      # Import global variables
import helpers

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
      gv.function_directory.add_variable('this-' + type, gv.current_block, Types.INT, None, memory_address, False, gv.current_class_block)
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
  variables_sizes = []
  for type in Types.primitives:
    address = gv.memory_manager.get_memory_address(type, MemoryTypes.SCOPE, gv.current_block, gv.current_class_block)
    variables_sizes.append(address)
  gv.subroutine_directory.add_next_memory_addresses(variables_sizes, gv.current_block, gv.current_class_block)
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
  if current_sub_call.get_param_count() != gv.subroutine_directory.get_param_count(current_sub_call.get_sub_name(), current_sub_call.get_block_name()):
    helpers.throw_error("Call not valid, less arguments than expected")
  
  quad = Quad(QuadOperations.GOSUB, current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  gv.quad_list.add(quad)

# checks if subroutine has return value or not, in case it was trying to be an assignment
def helper_sub_call_end(has_return_value):
  current_sub_call = gv.stack_sub_calls.pop()
  if type(current_sub_call) is ListMethodCall:
    list_type = current_sub_call.get_type()
    list_method_operator = current_sub_call.get_operator()
    if not has_return_value:
      return
    if list_method_operator in QuadOperations.list_method_no_return_value:
      helpers.throw_error("List method {} can't return a value.".format(list_method_operator))
      return
    temporal_type = QuadOperations.list_method_result_type[list_method_operator]
    if temporal_type is None:
      temporal_type = list_type
    temporal_operand = OperandItem(current_sub_call.get_return_temporal_address(), temporal_type)
    gv.stack_operands.push(temporal_operand)
    return

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

# Lists

def p_neural_list_decl(p):
  '''neural_list_decl :'''
  gv.current_is_list = True

def p_neural_list_init_value(p):
  '''neural_list_init_value :'''
  expression = gv.stack_operands.pop()
  gv.list_init_values.append(expression)

def p_neural_list_init_end(p):
  '''neural_list_init_end :'''
  list_item = gv.stack_operands.pop()
  list_address = list_item.get_value()
  list_type = list_item.get_type()

  for value in gv.list_init_values:
    if value.get_type() != list_type:
      helpers.throw_error("Type mismatch in initialization.")
    quad = Quad(QuadOperations.APPEND, list_address, list_type, value.get_value())
    gv.quad_list.add(quad)

  gv.list_init_values = []

def p_neural_list_method_start(p):
  '''neural_list_method_start :'''
  list_name = gv.sub_call_first_id  
  if gv.current_this:
    list_type, list_address, _, _ = gv.function_directory. \
      get_variable_item(list_name, Constants.GLOBAL_BLOCK, gv.current_class_block)
  else:
    list_type, list_address, _, _ = gv.function_directory. \
      get_variable_item_deep(list_name, gv.current_block, gv.current_class_block)
    
  gv.sub_call_first_id = None
  gv.current_this = False

  list_method_call = ListMethodCall(list_address, list_type)
  gv.stack_sub_calls.push(list_method_call)

def p_neural_list_operator(p):
  '''neural_list_operator :'''
  list_method_operator = p[-1]
  gv.stack_sub_calls.top().set_operator(list_method_operator)

def p_neural_list_method_arg(p):
  '''neural_list_method_arg :'''
  method_arg = gv.stack_operands.pop()
  gv.stack_sub_calls.top().add_arg(method_arg)

def p_neural_list_method_end(p):
  '''neural_list_method_end :'''
  list_method_call = gv.stack_sub_calls.top()
  list_address = list_method_call.get_address()
  list_type = list_method_call.get_type()
  list_method_operator = list_method_call.get_operator()
  method_args = list_method_call.get_args()

  if list_method_operator == QuadOperations.POP:
    if len(method_args) > 1:
      helpers.throw_error("More arguments than expected in {}".format(list_method_operator))
    if len(method_args) == 1 and (method_args[0].get_type() != Types.INT or method_args[0].is_list()):
      helpers.throw_error("Argument in {} must be of type {}".format(list_method_operator, Types.INT))
  
  if list_method_operator in QuadOperations.list_method_empty and len(method_args) > 0:
    helpers.throw_error("More arguments than expected in {}".format(list_method_operator))

  if list_method_operator in QuadOperations.list_method_expression:
    if len(method_args) != 1:
      helpers.throw_error("{} must have 1 argument".format(list_method_operator))
    expression_type = list_type if list_method_operator in QuadOperations.list_method_expression_type else Types.INT
    if method_args[0].get_type() != expression_type:
      helpers.throw_error("Argument in {} must be of type {}".format(list_method_operator, expression_type))

  if list_method_operator in QuadOperations.list_method_two_expression:
    if len(method_args) != 2:
      helpers.throw_error("{} must have 2 argument".format(list_method_operator))
    if method_args[0].get_type() != Types.INT:
      helpers.throw_error("First argument in {} must be of type {}".format(list_method_operator, Types.INT))
    if method_args[1].get_type() != list_type:
      helpers.throw_error("Second argument in {} must be of type {}".format(list_method_operator, expression_type))
    
  quad = Quad(list_method_operator, list_address)
  if list_method_operator in QuadOperations.list_method_require_list_type:
    quad.add_element(list_type)
  for arg in method_args:
    quad.add_element(arg.get_value())
  
  if list_method_operator in QuadOperations.list_method_return_value:
    memory_address = gv.memory_manager.get_memory_address(gv.stack_sub_calls.top().get_type(), MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    quad.add_element(memory_address)
    gv.stack_sub_calls.top().set_return_temporal_address(memory_address)

  gv.quad_list.add(quad)
