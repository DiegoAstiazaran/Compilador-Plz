# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens, lexer   # Import tokens and lexer defined in lexer
import globalVariables as gv      # Import global variables
from constants import Constants, Types, Operators, QuadOperations, MemoryTypes # Imports some constants
from structures import OperandPair, Quad, SubCall                 # Import OperandPair and Quad class
import helpers                    # Import helpers
import sys                        # TODO: delete

# Sets main grammar rule
start = 'program'

# Functions for all grammar rules
# Function name indicates what each of them are used for

def p_program(p):
  '''
  program : neural_global_block program_p block
  program_p : program_pp program_p
            | empty
  program_pp : decl_init
             | class
             | subroutine
  '''

def p_block(p):
  '''
  block : statement block
        | empty
  '''

def p_statement(p):
  '''
  statement : read
            | write
            | assignment
            | condition
            | cycle
            | return
            | sub_call
  '''

def p_sub_call(p):
  '''
  sub_call : ID neural_sub_call_first_id sub_call_p neural_sub_call sub_call_args DOT
  sub_call_p : MONEY neural_check_id_is_object ID neural_sub_call_second_id
             | empty
  '''

def p_sub_call_args(p):
  '''
  sub_call_args : L_PAREN sub_call_args_p R_PAREN neural_sub_call_args_end
  sub_call_args_p : expression neural_sub_call_arg sub_call_args_pp
                  | empty
  sub_call_args_pp : COMMA sub_call_args_p
                  | empty
  '''

def p_return(p):
  '''
  return : RETURN return_expression neural_return_expression DOT
  return_expression : expression neural_return_value
                    | empty
  '''

def p_class(p):
  '''
  class : CLASS CLASS_NAME neural_class_decl class_inheritance COLON class_block END neural_class_decl_end
  class_inheritance : UNDER CLASS_NAME neural_class_decl_inheritance
          | empty
  '''

def p_expression(p):
  '''
  expression : mini_expression neural_check_operator_stack_logical expression_p
  expression_p : logical expression
               | empty
  '''

def p_mini_expression(p):
  '''
  mini_expression : exp mini_expression_p neural_check_operator_stack_relational
  mini_expression_p : relational exp
                    | empty
  '''

def p_exp(p):
  '''
  exp : term neural_check_operator_stack_plus_minus exp_p
  exp_p : exp_pp exp
        | empty
  exp_pp : PLUS   neural_add_to_operator_stack
         | MINUS  neural_add_to_operator_stack
  '''

def p_term(p):
  '''
  term : factor neural_check_operator_stack_multiply_divide term_p
  term_p : term_pp term
         | empty
  term_pp : MULTIPLY  neural_add_to_operator_stack
          | DIVIDE    neural_add_to_operator_stack
  '''

def p_factor(p):
  '''
  factor : L_PAREN neural_operator_stack_push_false expression R_PAREN neural_operator_stack_pop_false
         | factor_p var_cte_2 neural_check_operator_stack_unary
  factor_p : PLUS   neural_add_to_operator_stack neural_read_unary_operator
           | MINUS  neural_add_to_operator_stack neural_read_unary_operator
           | NOT    neural_add_to_operator_stack neural_read_unary_operator
           | NOT_OP neural_add_to_operator_stack neural_read_unary_operator
           | empty
  '''

def p_class_block(p):
  '''
  class_block : class_block_attributes class_block_methods
  class_block_attributes : ATTRIBUTES COLON class_block_attributes_p
                         | empty
  class_block_methods : METHODS COLON class_block_methods_p
                      | empty
  class_block_attributes_p : class_block_p declaration neural_is_public_none class_block_attributes_p
                           | empty  
  class_block_methods_p : class_block_methods_constructor class_block_methods_pp
  class_block_methods_constructor : neural_class_decl_public constructor neural_is_public_none
  class_block_methods_pp : class_block_p subroutine neural_is_public_none class_block_methods_pp
                         | empty
  class_block_p : PUBLIC neural_class_decl_public
                | PRIVATE neural_class_decl_private
  '''

def p_declaration(p):
  '''
  declaration : declaration_p neural_check_operator_stack_equal DOT
  declaration_p : type ID neural_var_decl_id declaration_pp
                | DICT ID neural_var_decl_id
  declaration_pp : array_size declaration_ppp
                 | empty
  declaration_ppp : array_size
                  | empty
  '''

def p_array_size(p):
  '''
  array_size : L_PAREN CTE_I R_PAREN neural_array_decl
  '''

def p_decl_init(p):
  '''
  decl_init : decl_init_p neural_check_operator_stack_equal DOT
  decl_init_p : decl_init_var
              | decl_init_dict
              | decl_init_obj
  '''

def p_decl_init_var(p):
  '''
  decl_init_var : type ID neural_var_decl_id decl_init_var_p
  decl_init_var_p : decl_init_var_var
                  | decl_init_var_pp
  decl_init_var_var : EQUAL neural_add_to_operator_stack expression
                    | empty
  decl_init_var_pp : array_size decl_init_var_ppp
  decl_init_var_ppp : decl_init_var_array
                    | decl_init_var_matrix
  decl_init_var_array : EQUAL L_BRACKET array_content R_BRACKET
                      | empty
  array_content : expression array_content_p
  array_content_p : COMMA array_content
                  | empty
  decl_init_var_matrix : array_size decl_init_var_matrix_p
  decl_init_var_matrix_p : EQUAL L_BRACKET matrix_content R_BRACKET
                         | empty
  matrix_content : L_BRACKET array_content R_BRACKET matrix_content_p
  matrix_content_p : COMMA matrix_content
                   | empty
  '''
  # TODO: Put neural_add_to_operator_stack back after EQUAL in array and matrix initialization


def p_decl_init_dict(p):
  '''
  decl_init_dict : DICT ID neural_var_decl_id dict_init_dict_p
  dict_init_dict_p : EQUAL L_BRACKET initialization_dict R_BRACKET
                   | empty
  initialization_dict : var_cte_3 COLON expression initialization_dict_p
  initialization_dict_p : COMMA initialization_dict
                        | empty
  '''
  # TODO: Put neural_add_to_operator_stack back after EQUAL

def p_decl_init_obj(p):
  '''
  decl_init_obj : CLASS_NAME ID neural_var_decl_id EQUAL CLASS_NAME neural_constructor_call sub_call_args neural_sub_call_end_return_value
  '''
  # TODO: Put neural_add_to_operator_stack back after EQUAL

def p_assignment(p):
  '''
  assignment : ID neural_add_to_operand_stack_id assignment_obj assignment_access EQUAL neural_add_to_operator_stack expression neural_check_operator_stack_equal DOT
  assignment_obj : AT ID
                 | empty
  assignment_access : access
                    | empty
  '''

def p_constructor(p):
  '''
  constructor : SUB CLASS_NAME neural_sub_decl_id L_PAREN constructor_params R_PAREN COLON constructor_p block neural_sub_constructor_end END neural_global_block
  constructor_params : type ID neural_var_decl_id neural_param_decl constructor_params_p
                     | empty
  constructor_params_p : COMMA constructor_params
                       | empty
  constructor_p : decl_init constructor_p
                | empty
  '''

def p_relational(p):
  '''
  relational : L_THAN     neural_add_to_operator_stack
             | G_THAN     neural_add_to_operator_stack
             | NOT_EQ     neural_add_to_operator_stack
             | L_THAN_EQ  neural_add_to_operator_stack
             | G_THAN_EQ  neural_add_to_operator_stack
             | EQ_TO      neural_add_to_operator_stack
             | GT         neural_add_to_operator_stack
             | LT         neural_add_to_operator_stack
             | GTE        neural_add_to_operator_stack
             | LTE        neural_add_to_operator_stack
             | EQ         neural_add_to_operator_stack
             | NEQ        neural_add_to_operator_stack
  '''

def p_logical(p):
  '''
  logical : OR_OP   neural_add_to_operator_stack
          | AND_OP  neural_add_to_operator_stack
          | OR      neural_add_to_operator_stack
          | AND     neural_add_to_operator_stack
  '''

def p_var_cte_1(p):
  '''
  var_cte_1 : ID    neural_add_to_operand_stack_id
            | CTE_I neural_add_to_operand_stack_int
  '''

def p_var_cte_2(p):
  '''
  var_cte_2 : CTE_I   neural_add_to_operand_stack_int
            | CTE_F   neural_add_to_operand_stack_flt
            | CTE_STR neural_add_to_operand_stack_str
            | cte_b
            | id_calls
  '''

def p_id_calls(p):
  '''
  id_calls : ID neural_sub_call_first_id id_calls_p
  id_calls_p : access
             | neural_sub_call sub_call_args neural_sub_call_end_return_value
             | id_calls_method
             | id_calls_attribute
             | empty neural_id_calls_p_empty
  id_calls_method : MONEY neural_check_id_is_object ID neural_sub_call_second_id neural_sub_call sub_call_args neural_sub_call_end_return_value
  id_calls_attribute : AT neural_check_id_is_object ID neural_id_calls_p_empty id_calls_attribute_p
  id_calls_attribute_p : access
                       | empty
  '''

def p_var_cte_3(p):
  '''
  var_cte_3 : ID
            | CTE_I
            | CTE_STR
  '''

def p_cte_b(p):
  '''
  cte_b : TRUE  neural_add_to_operand_stack_bool
        | FALSE neural_add_to_operand_stack_bool
  '''

def p_subroutine(p):
  '''
  subroutine : SUB subroutine_return_type ID neural_sub_decl_id L_PAREN subroutine_params R_PAREN COLON subroutine_p block neural_sub_end neural_sub_constructor_end END neural_global_block
  subroutine_return_type : type
                         | VOID neural_decl_type
  subroutine_params : type ID neural_var_decl_id neural_param_decl subroutine_params_p
                    | empty
  subroutine_params_p : COMMA subroutine_params
                    | empty
  subroutine_p : decl_init subroutine_p
               | empty
  '''

def p_write(p):
  '''
  write : PRINT COLON write_p neural_write_new_line END
  write_p : expression neural_write_expression write_pp
  write_pp : neural_write_space COMMA write_p
           | empty
  '''

def p_condition(p):
  '''
  condition : IF neural_condition_if condition_p condition_else END neural_condition_end
  condition_p : expression neural_condition_new_quad COLON block neural_condition_end_block condition_elsif
  condition_elsif : ELSIF neural_condition_fill_quad condition_p
               | empty
  condition_else : ELSE neural_condition_else neural_condition_fill_quad COLON block
                | empty
  '''

def p_cycle(p):
  '''
  cycle : when
        | repeat
        | for
  '''

def p_operator(p):
  '''
  operator : PLUS     neural_add_to_operator_stack
           | MINUS    neural_add_to_operator_stack
           | MULTIPLY neural_add_to_operator_stack
           | DIVIDE   neural_add_to_operator_stack
  '''

def p_access(p):
  '''
  access : L_SQ_BRACKET expression R_SQ_BRACKET access_p
  access_p : L_SQ_BRACKET expression R_SQ_BRACKET
           | empty
  '''

def p_when(p):
  '''
  when : WHEN neural_when_before_expression expression REPEAT neural_when_repeat COLON block END neural_when_end
  '''

def p_repeat(p):
  '''
  repeat : REPEAT COLON neural_repeat_start block WHILE expression END neural_repeat_end
  '''

def p_for(p):
  '''
  for : FOR ID neural_for_id FROM for_p neural_for_assignment BY for_operator var_cte_1 WHILE neural_for_before_expression expression neural_for_after_expression COLON block END neural_for_end
  for_p : id_calls
        | CTE_I neural_add_to_operand_stack_int
        | CTE_F neural_add_to_operand_stack_flt
  for_operator : operator
               | empty
  '''

def p_read(p):
  '''
  read : READ COLON read_list END
  read_list : read_p read_list_p
  read_list_p : COMMA read_list
              | empty
  read_p : ID neural_read_stmt read_obj read_access
  read_obj : AT ID
           | empty
  read_access : access
              | empty
  '''

def p_type(p):
  '''
  type : INT neural_decl_type
       | FLT neural_decl_type
       | BOOL neural_decl_type
       | STR neural_decl_type
  '''

def p_empty(p):
  'empty :'
  pass

# Error rule for syntax errors
def p_error(p):
  print("Syntax error in input!")
  helpers.throw_error('Syntax error in input!"')

################################################################################
################                NEURALGIC POINTS                ################
################################################################################

#################################################
####### Function Directory Construction #########
#################################################

# Called when parsing starts and when subroutine ends
def p_neural_global_block(p):
  '''neural_global_block :'''
  # Set current block as global
  gv.current_block = Constants.GLOBAL_BLOCK

# Called after CLASS_NAME in class declaration
def p_neural_class_decl(p):
  '''neural_class_decl :'''
  gv.memory_manager.reset_class()
  gv.current_class_block = p[-1]
  gv.function_directory.add_block(gv.current_class_block, Constants.CLASS_BLOCK)
  gv.subroutine_directory.add_block(gv.current_class_block)

# Called at the end of class declaration
def p_neural_class_decl_end(p):
  '''neural_class_decl_end :'''
  gv.current_class_block = None

# Called after CLASS_NAME when inheriting a class
def p_neural_class_decl_inheritance(p):
  '''neural_class_decl_inheritance :'''
  class_name = p[-1]
  gv.function_directory.check_class(class_name)

# Called after PRIVATE in public section of class declaration
def p_neural_class_decl_private(p):
  '''neural_class_decl_private :'''
  gv.current_is_public = False

# Called after PUBLIC in public section of class declaration
def p_neural_class_decl_public(p):
  '''neural_class_decl_public :'''
  gv.current_is_public = True

#
def p_neural_is_public_none(p):
  '''neural_is_public_none :'''
  gv.current_is_public = None

# Called after ID in every declaration or initialization
# It can be in decl_init, parameter declaration or attribute declaration
def p_neural_var_decl_id(p):
  '''neural_var_decl_id :'''
  if gv.current_last_type == None:
    # Second previous element in p will be stored; DICT or CLASS_NAME
    gv.current_last_type = p[-2]
  gv.current_last_id = p[-1]

  memory_address = gv.memory_manager.get_memory_address(gv.current_last_type, MemoryTypes.SCOPE, gv.current_block, gv.current_class_block)
  
  # TODO: remove
  if memory_address is None:
    memory_address = gv.current_last_id

  gv.function_directory.add_variable(gv.current_last_id, gv.current_block, gv.current_last_type, gv.current_is_public, memory_address, gv.current_class_block)
  # Add operand to operand stack in case it is a initialization
  add_to_operand_stack(memory_address, gv.current_last_type)

  gv.current_param_type = gv.current_last_type
  gv.current_last_type = None

def p_neural_param_decl(p):
  '''neural_param_decl :'''
  gv.stack_operands.pop()
  gv.subroutine_directory.add_param(gv.current_block, gv.current_param_type, gv.current_class_block)

# Called after each primitive type
def p_neural_decl_type(p):
  '''neural_decl_type :'''
  gv.current_last_type = p[-1]

def p_neural_array_decl(p):
  '''neural_array_decl :'''
  gv.function_directory.add_dimension_to_variable(gv.current_last_id, gv.current_block, gv.current_class_block)

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

#################################################
#######  Expression Quad Constructions  #########
#################################################

### Check operator stack

def p_neural_check_operator_stack_relational(p):
  '''neural_check_operator_stack_relational :'''
  check_operator_stack(Operators.relational)

def p_neural_check_operator_stack_logical(p):
  '''neural_check_operator_stack_logical :'''
  check_operator_stack(Operators.logical)

def p_neural_check_operator_stack_plus_minus(p):
  '''neural_check_operator_stack_plus_minus :'''
  check_operator_stack(Operators.plus_minus)

def p_neural_check_operator_stack_multiply_divide(p):
  '''neural_check_operator_stack_multiply_divide :'''
  check_operator_stack(Operators.multiply_divide)

def p_neural_check_operator_stack_unary(p):
  '''neural_check_operator_stack_unary :'''
  check_operator_stack()

def p_neural_check_operator_stack_equal(p):
  '''neural_check_operator_stack_equal :'''
  first = gv.stack_operands.pop()
  if not gv.stack_operators.empty() and gv.stack_operators.top() == Operators.EQUAL:
    operand_id = gv.stack_operands.pop()
    operator = gv.stack_operators.pop()
    if first.get_type() != operand_id.get_type():
      helpers.throw_error('Type mismatch')
    quad = Quad(operator, first.get_value(), operand_id.get_value())
    gv.quad_list.add(quad)

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

    if result_type == None:
      helpers.throw_error('Type mismatch on operator ')

    result_value = gv.memory_manager.get_memory_address(result_type, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
    if operand_left is None:
      quad = Quad(operator, operand_right.get_value(), result_value)
    else:
      quad = Quad(operator, operand_left.get_value(), operand_right.get_value(), result_value)

    gv.quad_list.add(quad)
    result = OperandPair(result_value, result_type)
    gv.stack_operands.push(result)
    gv.read_unary_operator = False

### Add to operand stack

def p_neural_add_to_operand_stack_int(p):
  '''neural_add_to_operand_stack_int :'''
  operand_value = p[-1]
  operand_type = Types.INT
  operand_value = gv.memory_manager.get_constant_memory_address(operand_value, operand_type)
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_flt(p):
  '''neural_add_to_operand_stack_flt :'''
  operand_value = p[-1]
  operand_type = Types.FLT
  operand_value = gv.memory_manager.get_constant_memory_address(operand_value, operand_type)
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_str(p):
  '''neural_add_to_operand_stack_str :'''
  operand_value = p[-1]
  operand_type = Types.STR
  operand_value = gv.memory_manager.get_constant_memory_address(operand_value, operand_type)
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_bool(p):
  '''neural_add_to_operand_stack_bool :'''
  operand_value = p[-1]
  operand_type = Types.BOOL
  operand_value = gv.memory_manager.get_constant_memory_address(operand_value, operand_type)
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_id(p):
  '''neural_add_to_operand_stack_id :'''
  id_name = p[-1]
  id_type, id_name = gv.function_directory.get_variable_type_address(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type)

def p_neural_id_calls_p_empty(p):
  '''neural_id_calls_p_empty :'''
  id_name = gv.sub_call_first_id
  id_type, id_name = gv.function_directory.get_variable_type_address(id_name, gv.current_block, gv.current_class_block)
  add_to_operand_stack(id_name, id_type)
  gv.sub_call_first_id = None

def add_to_operand_stack(operand_value, operand_type):
  gv.stack_operands.push(OperandPair(operand_value, operand_type))

### Modify operator stack

def p_neural_add_to_operator_stack(p):
  '''neural_add_to_operator_stack :'''
  operator = p[-1]
  gv.stack_operators.push(operator)

def p_neural_read_unary_operator(p):
  '''neural_read_unary_operator :'''
  gv.read_unary_operator = True

def p_neural_operator_stack_push_false(p):
  '''neural_operator_stack_push_false :'''
  gv.stack_operators.push("(")

def p_neural_operator_stack_pop_false(p):
  '''neural_operator_stack_pop_false :'''
  gv.stack_operators.pop()

### Write

def p_neural_write_expression(p):
  '''neural_write_expression :'''
  expression = gv.stack_operands.pop()
  quad = Quad(QuadOperations.WRITE, expression.get_value())
  gv.quad_list.add(quad)

def p_neural_write_new_line(p):
  '''neural_write_new_line :'''
  quad = Quad(QuadOperations.WRITE_NEW_LINE)
  gv.quad_list.add(quad)

def p_neural_write_space(p):
  '''neural_write_space :'''
  quad = Quad(QuadOperations.WRITE_SPACE)
  gv.quad_list.add(quad)

### Read

def p_neural_read(p):
  '''neural_read_stmt :'''
  id_name = p[-1]
  id_type, id_name = gv.function_directory.get_variable_type_address(id_name, gv.current_block, gv.current_class_block)
  if id_type not in Types.primitives:
    helpers.throw_error("Cannot assign input to " + id_name)
  quad = Quad(QuadOperations.READ, id_name)
  gv.quad_list.add(quad)

### Return

def p_neural_return_value(p):
  '''neural_return_value :'''
  gv.current_return_has_value = True

def p_neural_return_expression(p):
  '''neural_return_expression :'''
  if gv.current_block == Constants.GLOBAL_BLOCK:
    helpers.throw_error("Syntax error, return statement must be in subroutine")

  current_sub_type = gv.function_directory.get_sub_type(gv.current_block, gv.current_class_block)
  if current_sub_type == Constants.CONSTRUCTOR_BLOCK:
    helpers.throw_error("Invalid return statement in constructor")

  quad = Quad(QuadOperations.RETURN)

  if gv.current_return_has_value:
    expression = gv.stack_operands.pop()
    return_value_type = expression.get_type()
    quad.add_element(expression.get_value())
  else:
    return_value_type = Types.VOID

  if return_value_type != current_sub_type:
    if current_sub_type == Types.VOID:
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
  current_sub_type = gv.function_directory.get_sub_type(gv.current_block, gv.current_class_block)
  if current_sub_type != Types.VOID and current_sub_type != Constants.CONSTRUCTOR_BLOCK and not gv.current_sub_has_return_stmt:
    helpers.throw_error("Subroutine must have return statement")
  # TODO: generate RETURN for constructor
  if not gv.current_sub_has_return_stmt:
    quad = Quad(QuadOperations.RETURN)
    gv.quad_list.add(quad)
  gv.current_sub_has_return_stmt = False

def p_neural_sub_constructor_end(p):
  '''neural_sub_constructor_end :'''
  gv.function_directory.free_memory(gv.current_block, gv.current_class_block)

### Condition

def p_neural_condition_if(p):
  '''neural_condition_if :'''
  gv.stack_jumps.push(Constants.FALSE_BOTTOM_IF_CONDITION)

def p_neural_condition_new_quad(p):
  '''neural_condition_new_quad :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

def p_neural_condition_fill_quad(p):
  '''neural_condition_fill_quad :'''
  end_block_index = gv.stack_jumps.pop()
  quad_index = gv.stack_jumps.pop()
  next_quad_index = gv.quad_list.next()
  if not gv.current_condition_has_else and gv.condition_end:
    next_quad_index -= 1
  gv.quad_list.add_element_to_quad(quad_index, next_quad_index)
  gv.stack_jumps.push(end_block_index)

def p_neural_condition_else(p):
  '''neural_condition_else :'''
  gv.current_condition_has_else = True

def p_neural_condition_end(p):
  '''neural_condition_end :'''
  gv.condition_end = True
  if not gv.current_condition_has_else:
    p_neural_condition_fill_quad(p)
  last_goto_index = gv.stack_jumps.top()
  if not gv.current_condition_has_else:
    gv.quad_list.erase(last_goto_index)
    gv.stack_jumps.pop()
  while gv.stack_jumps.top() != Constants.FALSE_BOTTOM_IF_CONDITION:
     quad_index = gv.stack_jumps.pop()
     gv.quad_list.add_element_to_quad(quad_index, gv.quad_list.next())
  gv.stack_jumps.pop()
  gv.condition_end = False

def p_neural_condition_end_block(p):
  '''neural_condition_end_block :'''
  quad = Quad(QuadOperations.GOTO)
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)
  gv.quad_list.add(quad)

### When

def p_neural_when_before_expression(p):
  '''neural_when_before_expression :'''
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)

def p_neural_when_repeat(p):
  '''neural_when_repeat :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

def p_neural_when_end(p):
  '''neural_when_end :'''
  goto_f_index = gv.stack_jumps.pop()
  goto_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO, goto_index)
  gv.quad_list.add(quad)
  next_index = gv.quad_list.next()
  gv.quad_list.add_element_to_quad(goto_f_index, next_index)

### Repeat

def p_neural_repeat_start(p):
  '''neural_repeat_start :'''
  next_quad = gv.quad_list.next()
  gv.stack_jumps.push(next_quad)

def p_neural_repeat_end(p):
  '''neural_repeat_end :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
      helpers.throw_error("Condition must be boolean")
  goto_t_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO_T, condition.get_value(), goto_t_index)
  gv.quad_list.add(quad)

### For

def p_neural_for_id(p):
  '''neural_for_id :'''
  id_name = p[-1]
  id_type, id_name = gv.function_directory.get_variable_type_address(id_name, gv.current_block, gv.current_class_block)
  if id_type != Types.INT and id_type != Types.FLT:
    helpers.throw_error("Variable must be integer or float")
  add_to_operand_stack(id_name, id_type)

def p_neural_for_assignment(p):
  '''neural_for_assignment :'''
  value_to_assign = gv.stack_operands.pop()
  id = gv.stack_operands.top()
  quad = Quad(Operators.EQUAL, value_to_assign.get_value(), id.get_value())
  gv.quad_list.add(quad)

def p_neural_for_before_expression(p):
  '''neural_for_before_expression :'''
  gv.current_for_operator = Operators.PLUS if gv.stack_operators.empty() else gv.stack_operators.pop()
  gv.stack_jumps.push(gv.quad_list.next())

def p_neural_for_after_expression(p):
  '''neural_for_after_expression :'''
  condition = gv.stack_operands.pop()
  if condition.get_type() != Types.BOOL:
    helpers.throw_error("Condition must be boolean")
  quad = Quad(QuadOperations.GOTO_F, condition.get_value())
  gv.stack_jumps.push(gv.quad_list.next())
  gv.quad_list.add(quad)

def p_neural_for_end(p):
  '''neural_for_end :'''
  change_value = gv.stack_operands.pop()
  id = gv.stack_operands.pop()
  quad = Quad(gv.current_for_operator, id.get_value(), change_value.get_value(), id.get_value())
  gv.quad_list.add(quad)

  goto_f_index = gv.stack_jumps.pop()
  goto_index = gv.stack_jumps.pop()
  quad = Quad(QuadOperations.GOTO, goto_index)
  gv.quad_list.add(quad)
  next_index = gv.quad_list.next()
  gv.quad_list.add_element_to_quad(goto_f_index, next_index)

### Subroutine calls

def p_neural_sub_call_first_id(p):
  '''neural_sub_call_first_id :'''
  gv.sub_call_first_id = p[-1]

def p_neural_sub_call_second_id(p):
  '''neural_sub_call_second_id :'''
  gv.sub_call_second_id = p[-1]

def p_neural_sub_call(p):
  '''neural_sub_call :'''
  if gv.sub_call_second_id == None:
    sub_call_name = gv.sub_call_first_id
    sub_call_class_name = None
  else:
    sub_call_name = gv.sub_call_second_id
    object_name = gv.sub_call_first_id
    sub_call_class_name, _ = gv.function_directory.get_variable_type_address(object_name, gv.current_block, gv.current_class_block)

  sub_call = SubCall(sub_call_name, sub_call_class_name)
  gv.stack_sub_calls.push(sub_call)

  if not gv.subroutine_directory.check_sub_exists(sub_call_name, sub_call_class_name):
    helpers.throw_error("Method " + sub_call_name + " doesn't exist.")
  
  if sub_call_class_name != None and gv.current_class_block != sub_call_class_name and not gv.subroutine_directory.is_method_public(sub_call_name, sub_call_class_name):
    helpers.throw_error("Method " + sub_call_name + " is not public and cannot be called in current location.")
  
  quad = Quad(QuadOperations.ERA, sub_call_class_name, sub_call_name)
  gv.quad_list.add(quad)

  gv.sub_call_first_id = None
  gv.sub_call_second_id = None

def p_neural_sub_call_arg(p):
  '''neural_sub_call_arg :'''
  arg = gv.stack_operands.pop()
  current_sub_call = gv.stack_sub_calls.top()
  param_count = current_sub_call.get_param_count()
  if not gv.subroutine_directory.check_arg(arg.get_type(), param_count, current_sub_call.get_sub_name(), current_sub_call.get_block_name()):
    helpers.throw_error("Type mismatch in argument #{}, expected {}".format(param_count + 1, gv.subroutine_directory.get_param_type(param_count, current_sub_call.get_sub_name(), current_sub_call.get_block_name())) )
  
  quad = Quad(QuadOperations.PARAM, arg.get_value(), param_count)
  gv.quad_list.add(quad)

  param_count = gv.stack_sub_calls.top().add_param_count()

def p_neural_sub_call_args_end(p):
  '''neural_sub_call_args_end :'''
  current_sub_call = gv.stack_sub_calls.top()  
  if current_sub_call.get_param_count() != gv.subroutine_directory.get_param_count(current_sub_call.get_sub_name(), current_sub_call.get_block_name()):
    helpers.throw_error("Call not valid, less arguments than expected")
  
  quad = Quad(QuadOperations.GOSUB, current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  gv.quad_list.add(quad)

def p_neural_sub_call_end_return_value(p):
  '''neural_sub_call_end_return_value :'''
  current_sub_call = gv.stack_sub_calls.pop()
  return_type = gv.subroutine_directory.get_sub_type(current_sub_call.get_sub_name(), current_sub_call.get_block_name())
  temporal = gv.memory_manager.get_memory_address(return_type, MemoryTypes.TEMPORAL, gv.current_block, gv.current_class_block)
  if gv.function_directory.check_id_is_class(return_type):
    # TODO: fix this for constructor
    return_value = gv.temporal_memory.get_available()
  else:
    return_value = gv.memory_manager.get_last_global(return_type)
    
  quad = Quad(Operators.EQUAL, return_value, temporal)
  gv.quad_list.add(quad)
  temporal_operand = OperandPair(temporal, return_type)
  gv.stack_operands.push(temporal_operand)

def p_neural_constructor_call(p):
  '''neural_constructor_call :'''
  sub_call_name = p[-1]
  sub_call_class_name = p[-1]

  sub_call = SubCall(sub_call_name, sub_call_class_name)
  gv.stack_sub_calls.push(sub_call)

  if not gv.subroutine_directory.check_block_exists(sub_call_class_name):
    helpers.throw_error("Class " + sub_call_class_name + " doesn't exist.")
  
  quad = Quad(QuadOperations.ERA, sub_call_class_name, sub_call_name)
  gv.quad_list.add(quad)

def p_neural_check_id_is_object(p):
  '''neural_check_id_is_object :'''
  id_name = gv.sub_call_first_id
  id_type, _ = gv.function_directory.get_variable_type_address(id_name, gv.current_block, gv.current_class_block)
  if not gv.function_directory.check_id_is_class(id_type):
    helpers.throw_error(id_name + " is not an object")

### Other

# Use for debugging
# TODO: delete
def p_neural_new_line(p):
  '''neural_new_line :'''
  line = lexer.lineno
  if line not in gv.lines_read:
    print('Line #%d\n' % (line) )
  gv.lines_read.append(line)

# Build the parser
parser = yacc.yacc()

# Execution of parser with a filename
while True:
  try:
      # file = input('Filename: ')
      file = 'nice_test.plz'
      with open(file, 'r') as myfile:
          s = myfile.read()
  except EOFError:
      break
  if not file: continue
  result = parser.parse(s)
  print(result)
  # print(gv.quad_list)
  gv.quad_list.print_with_number()
  del sys.modules['globalVariables']
  import globalVariables as gv
  break # remove this break to loop the tests
  # gv.function_directory.output()
