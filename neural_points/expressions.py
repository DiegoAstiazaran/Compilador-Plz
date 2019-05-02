from constants import Constants, Operators, Types, MemoryTypes, QuadOperations
from structures import Quad, OperandItem
import global_variables as gv      # Import global variables
import helpers
from lexer import lexer # TODO:delete all lexer imports

# Called before every expression so two expressions are not combined
def p_neural_expression_start(p):
  '''neural_expression_start :'''
  gv.stack_operators.push(Constants.FALSE_BOTTOM_EXPRESSION)

# Called after expression
def p_neural_expression_end(p):
  '''neural_expression_end :'''
  gv.stack_operators.pop()

### Add to operand stack

# Called after constants int in expression
def p_neural_add_to_operand_stack_int(p):
  '''neural_add_to_operand_stack_int :'''
  operand_value = p[-1]
  operand_type = Types.INT
  add_to_operand_stack_constant(operand_value, operand_type)

# Called after constants flt in expression
def p_neural_add_to_operand_stack_flt(p):
  '''neural_add_to_operand_stack_flt :'''
  operand_value = p[-1]
  operand_type = Types.FLT
  add_to_operand_stack_constant(operand_value, operand_type)

# Called after constants str in expression
def p_neural_add_to_operand_stack_str(p):
  '''neural_add_to_operand_stack_str :'''
  operand_value = p[-1]
  operand_type = Types.STR
  add_to_operand_stack_constant(operand_value, operand_type)

# Called after constants bool in expression
def p_neural_add_to_operand_stack_bool(p):
  '''neural_add_to_operand_stack_bool :'''
  operand_value = p[-1]
  operand_type = Types.BOOL
  add_to_operand_stack_constant(operand_value, operand_type)

# Called after id's in expression
def p_neural_add_to_operand_stack_id(p):
  '''neural_add_to_operand_stack_id :'''
  id_name = p[-1]
  id_type, id_name, id_block, id_class = gv.function_directory.get_variable_item_deep(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type, id_block, id_class)

# Helper to add constants to operand stack
# Changes constant to memory_address
def add_to_operand_stack_constant(operand_value, operand_type):
  operand_value = gv.memory_manager.get_constant_memory_address(operand_value, operand_type)
  add_to_operand_stack(operand_value, operand_type)

# Helper to insert OperandItem to operand stack
def add_to_operand_stack(operand_value, operand_type, block_name = None, class_name = None):
  gv.stack_operands.push(OperandItem(operand_value, operand_type, block_name, class_name))

### Check operator stack

# Checks if operator stack top is relational
def p_neural_check_operator_stack_relational(p):
  '''neural_check_operator_stack_relational :'''
  check_operator_stack(Operators.relational)

# Checks if operator stack top is logical
def p_neural_check_operator_stack_logical(p):
  '''neural_check_operator_stack_logical :'''
  check_operator_stack(Operators.logical)

# Checks if operator stack top is plus or minus
def p_neural_check_operator_stack_plus_minus(p):
  '''neural_check_operator_stack_plus_minus :'''
  check_operator_stack(Operators.plus_minus)

# Checks if operator stack top is multiply or divide
def p_neural_check_operator_stack_multiply_divide(p):
  '''neural_check_operator_stack_multiply_divide :'''
  check_operator_stack(Operators.multiply_divide)

# Checks if operator stack top is unary
def p_neural_check_operator_stack_unary(p):
  '''neural_check_operator_stack_unary :'''
  check_operator_stack()

# Helper to check if top of operator stack is what we're looking for
# operators_list is None when checking unary_operator
def check_operator_stack(operators_list = None):
  # first part of condition is for unary operators
  # second part is for the rest of the operators
  if gv.read_unary_operator or (operators_list and not gv.stack_operators.empty() and gv.stack_operators.top() in operators_list):
    operator = gv.stack_operators.pop()
    operand_right = gv.stack_operands.pop()
    operand_left = gv.stack_operands.pop() if operators_list else None

    if operand_left is None:
      result_type = gv.semantic_cube.validate_type(operator, operand_right.get_type())
    else:
      result_type = gv.semantic_cube.validate_type(operator, operand_left.get_type(), operand_right.get_type())

    if result_type is None:
      helpers.throw_error('Type mismatch on operator ')

    result_value = gv.memory_manager.get_memory_address(result_type, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    if operand_left is None:
      quad = Quad(operator, operand_right.get_value(), result_value)
    else:
      if operator == Operators.DIVIDE:
        quad = Quad(QuadOperations.CHECK_DIV, operand_right.get_value())
        gv.quad_list.add(quad)
      quad = Quad(operator, operand_left.get_value(), operand_right.get_value(), result_value)

    gv.quad_list.add(quad)
    result = OperandItem(result_value, result_type)
    gv.stack_operands.push(result)
    gv.read_unary_operator = False

# Checks if operator stack top is equal
# This will pop the last operand from the stack if = is not found
def p_neural_check_operator_stack_equal(p):
  '''neural_check_operator_stack_equal :'''
  first = gv.stack_operands.pop()
  if not gv.stack_operators.empty() and gv.stack_operators.top() == Operators.EQUAL:
    operand_id = gv.stack_operands.pop()
    # TODO: cheecar esto
    # operand_id_type = operand_id.get_type() if operand_id.get_type() in Types.primitives else operand_id.get_type()[0]
    operator = gv.stack_operators.pop()
    if first.get_type() != operand_id.get_type():
      helpers.throw_error('Type mismatch')
    quad = Quad(operator, first.get_value(), operand_id.get_value())
    gv.quad_list.add(quad)

### Modify operator stack

def p_neural_add_to_operator_stack(p):
  '''neural_add_to_operator_stack :'''
  operator = p[-1]
  gv.stack_operators.push(operator)

def p_neural_read_unary_operator(p):
  '''neural_read_unary_operator :'''
  operator = gv.stack_operators.top()
  if operator == Operators.PLUS:
    gv.stack_operators.pop()
    new_operator = QuadOperations.PLUS_UNARY
    gv.stack_operators.push(new_operator)
  elif operator == Operators.MINUS:
    gv.stack_operators.pop()
    new_operator = QuadOperations.MINUS_UNARY
    gv.stack_operators.push(new_operator)
  gv.read_unary_operator = True

# TODO: delete
# def p_neural_operator_stack_push_false(p):
#   '''neural_operator_stack_push_false :'''
#   gv.stack_operators.push("(")

# def p_neural_operator_stack_pop_false(p):
#   '''neural_operator_stack_pop_false :'''
#   gv.stack_operators.pop()
