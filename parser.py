# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens, lexer   # Import tokens and lexer defined in lexer
from parserDebug import *         # Import functions to debug parser
import globalVariables as gv      # Import global variables
from constants import Constants, Types, Operators, QuadOperations # Imports some constants
from structures import OperandPair, Quad  # Import OperandPair and Quad class
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
  program_debug(p, gv.parse_debug)

def p_block(p):
  '''
  block : statement block
        | empty
  '''
  block_debug(p, gv.parse_debug)

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
  statement_debug(p, gv.parse_debug)

def p_sub_call(p):
  '''
  sub_call : ID sub_call_p sub_call_args DOT
  sub_call_p : MONEY ID
             | empty
  '''
  sub_call_debug(p, gv.parse_debug)

def p_sub_call_args(p):
  '''
  sub_call_args : L_PAREN sub_call_args_p R_PAREN
  sub_call_args_p : expression sub_call_args_pp
                  | empty
  sub_call_args_pp : COMMA sub_call_args_p
                  | empty
  '''
  sub_call_args_debug(p, gv.parse_debug)

def p_return(p):
  '''
  return : RETURN return_expression neural_return_expression DOT
  return_expression : expression neural_return_value
                    | empty
  '''
  return_debug(p, gv.parse_debug)

def p_class(p):
  '''
  class : CLASS CLASS_NAME neural_class_decl class_p COLON class_block END neural_class_decl_end
  class_p : UNDER CLASS_NAME neural_class_decl_inheritance
          | empty
  '''
  class_debug(p, gv.parse_debug)

def p_expression(p):
  '''
  expression : mini_expression neural_check_operator_stack_logical expression_p
  expression_p : logical expression
               | empty
  '''
  expression_debug(p, gv.parse_debug)

def p_mini_expression(p):
  '''
  mini_expression : exp mini_expression_p neural_check_operator_stack_relational
  mini_expression_p : relational exp
                    | empty
  '''
  mini_expression_debug(p, gv.parse_debug)

def p_exp(p):
  '''
  exp : term neural_check_operator_stack_plus_minus exp_p
  exp_p : exp_pp exp
        | empty
  exp_pp : PLUS   neural_add_to_operator_stack
         | MINUS  neural_add_to_operator_stack
  '''
  exp_debug(p, gv.parse_debug)

def p_term(p):
  '''
  term : factor neural_check_operator_stack_multiply_divide term_p
  term_p : term_pp term
         | empty
  term_pp : MULTIPLY  neural_add_to_operator_stack
          | DIVIDE    neural_add_to_operator_stack
  '''
  term_debug(p, gv.parse_debug)

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
  factor_debug(p, gv.parse_debug)

def p_class_block(p):
  '''
  class_block : constructor class_block_private class_block_public
  class_block_private : private
                      | empty
  class_block_public : public
                     | empty
  '''
  class_block_debug(p, gv.parse_debug)

def p_private(p):
  '''
  private : PRIVATE neural_class_decl_private COLON private_declaration private_sub END neural_class_decl_section_end
  private_declaration : declaration private_declaration
                      | empty
  private_sub : subroutine private_sub
              | empty
  '''
  private_debug(p, gv.parse_debug)

def p_public(p):
  '''
  public : PUBLIC neural_class_decl_public COLON public_declaration public_sub END neural_class_decl_section_end
  public_declaration : declaration public_declaration
                     | empty
  public_sub : subroutine public_sub
             | empty
  '''
  public_debug(p, gv.parse_debug)

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
  declaration_debug(p, gv.parse_debug)

def p_array_size(p):
  '''
  array_size : L_PAREN CTE_I R_PAREN neural_array_decl
  '''
  array_size_debug(p, gv.parse_debug)

def p_decl_init(p):
  '''
  decl_init : decl_init_p neural_check_operator_stack_equal DOT
  decl_init_p : decl_init_var
              | decl_init_dict
              | decl_init_obj
  '''
  decl_init_debug(p, gv.parse_debug)

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

  decl_init_var_debug(p, gv.parse_debug)

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
  decl_init_dict_debug(p, gv.parse_debug)

def p_decl_init_obj(p):
  '''
  decl_init_obj : CLASS_NAME ID neural_var_decl_id EQUAL CLASS_NAME sub_call_args
  '''
  # TODO: Put neural_add_to_operator_stack back after EQUAL
  decl_init_obj_debug(p, gv.parse_debug)

def p_assignment(p):
  '''
  assignment : ID neural_add_to_operand_stack_id assignment_obj assignment_access EQUAL neural_add_to_operator_stack expression neural_check_operator_stack_equal DOT
  assignment_obj : AT ID
                 | empty
  assignment_access : access
                    | empty
  '''
  assignment_debug(p, gv.parse_debug)

def p_constructor(p):
  '''
  constructor : SUB CLASS_NAME neural_sub_decl_id L_PAREN constructor_params R_PAREN COLON constructor_p block END neural_global_block
  constructor_params : type ID neural_var_decl_id constructor_params_p
                     | empty
  constructor_params_p : COMMA constructor_params
                       | empty
  constructor_p : decl_init constructor_p
                | empty
  '''
  constructor_debug(p, gv.parse_debug)

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
  relational_debug(p, gv.parse_debug)

def p_logical(p):
  '''
  logical : OR_OP   neural_add_to_operator_stack
          | AND_OP  neural_add_to_operator_stack
          | OR      neural_add_to_operator_stack
          | AND     neural_add_to_operator_stack
  '''
  logical_debug(p, gv.parse_debug)

def p_var_cte_1(p):
  '''
  var_cte_1 : ID
            | CTE_I
  '''
  var_cte_1_debug(p, gv.parse_debug)

def p_var_cte_2(p):
  '''
  var_cte_2 : CTE_I   neural_add_to_operand_stack_int
            | CTE_F   neural_add_to_operand_stack_flt
            | CTE_STR neural_add_to_operand_stack_str
            | cte_b
            | id_calls
  '''
  var_cte_2_debug(p, gv.parse_debug)

def p_id_calls(p):
  '''
  id_calls : ID neural_add_to_operand_stack_id id_calls_p
  id_calls_p : access
             | sub_call_args
             | id_calls_method
             | id_calls_attribute
             | empty
  id_calls_method : MONEY ID sub_call_args
  id_calls_attribute : AT ID id_calls_attribute_p
  id_calls_attribute_p : access
                       | empty
  '''
  # TODO: move neural_add_to_operand_stack_id
  id_calls_debug(p, gv.parse_debug)

def p_var_cte_3(p):
  '''
  var_cte_3 : var_cte_1
            | CTE_STR
  '''
  var_cte_3_debug(p, gv.parse_debug)

def p_cte_b(p):
  '''
  cte_b : TRUE  neural_add_to_operand_stack_bool
        | FALSE neural_add_to_operand_stack_bool
  '''
  cte_b_debug(p, gv.parse_debug)

def p_subroutine(p):
  '''
  subroutine : SUB subroutine_return_type ID neural_sub_decl_id L_PAREN subroutine_params R_PAREN COLON subroutine_p block neural_sub_end END neural_global_block
  subroutine_return_type : type
                         | VOID neural_decl_type
  subroutine_params : type ID neural_var_decl_id subroutine_params_p
                    | empty
  subroutine_params_p : COMMA subroutine_params
                    | empty
  subroutine_p : decl_init subroutine_p
               | empty
  '''
  subroutine_debug(p, gv.parse_debug)

def p_write(p):
  '''
  write : PRINT COLON write_p neural_write_new_line END
  write_p : expression neural_write_expression write_pp
  write_pp : neural_write_space COMMA write_p
           | empty
  '''
  write_debug(p, gv.parse_debug)

def p_condition(p):
  '''
  condition : IF neural_condition_if condition_p condition_else END neural_condition_end
  condition_p : expression neural_condition_new_quad COLON block neural_condition_end_block condition_elsif
  condition_elsif : ELSIF neural_condition_fill_quad condition_p
               | empty
  condition_else : ELSE neural_condition_else neural_condition_fill_quad COLON block
                | empty
  '''
  condition_debug(p, gv.parse_debug)

def p_cycle(p):
  '''
  cycle : when
        | repeat
        | for
  '''
  cycle_debug(p, gv.parse_debug)

def p_operator(p):
  '''
  operator : PLUS
           | MINUS
           | MULTIPLY
           | DIVIDE
  '''
  operator_debug(p, gv.parse_debug)

def p_access(p):
  '''
  access : L_SQ_BRACKET expression R_SQ_BRACKET access_p
  access_p : L_SQ_BRACKET expression R_SQ_BRACKET
           | empty
  '''
  access_debug(p, gv.parse_debug)

def p_when(p):
  '''
  when : WHEN neural_when_before_expression expression REPEAT neural_when_repeat COLON block END neural_when_end
  '''
  when_debug(p, gv.parse_debug)

def p_repeat(p):
  '''
  repeat : REPEAT COLON block WHILE expression END
  '''
  repeat_debug(p, gv.parse_debug)

def p_for(p):
  '''
  for : FOR ID FROM for_p BY for_operator var_cte_1 WHILE expression COLON block END
  for_p : id_calls
        | CTE_I
  for_operator : operator
               | empty
  '''
  for_debug(p, gv.parse_debug)

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
  read_debug(p, gv.parse_debug)

def p_type(p):
  '''
  type : INT neural_decl_type
       | FLT neural_decl_type
       | BOOL neural_decl_type
       | STR neural_decl_type
  '''
  type_debug(p, gv.parse_debug)

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
  gv.current_class_block = p[-1]
  gv.function_directory.add_block(gv.current_class_block, Constants.CLASS_BLOCK)

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

# Called at the end of private or public section of class declaration
def p_neural_class_decl_section_end(p):
  '''neural_class_decl_section_end : '''
  gv.current_is_public = None

# Called after ID in every declaration or initialization
# It can be in decl_init, parameter declaration or attribute declaration
def p_neural_var_decl_id(p):
  '''neural_var_decl_id :'''
  if gv.current_last_type == None:
    # Second previous element in p will be stored; DICT or CLASS_NAME
    gv.current_last_type = p[-2]
  gv.current_last_id = p[-1]
  gv.function_directory.add_variable(gv.current_last_id, gv.current_block, gv.current_last_type, gv.current_is_public, gv.current_class_block)
  # Add operand to operand stack in case it is a initialization
  add_to_operand_stack(gv.current_last_id, gv.current_last_type)

  gv.current_last_type = None

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
  gv.current_block = p[-1]
  if gv.current_last_type == None:
    gv.current_last_type = Constants.CONSTRUCTOR_BLOCK
  gv.function_directory.add_block(gv.current_block, gv.current_last_type, gv.current_is_public, gv.current_class_block)
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

    result_value = gv.temporal_memory.get_available()
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
  operand_type = "int"
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_flt(p):
  '''neural_add_to_operand_stack_flt :'''
  operand_value = p[-1]
  operand_type = "flt"
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_str(p):
  '''neural_add_to_operand_stack_str :'''
  operand_value = p[-1]
  operand_type = "str"
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_bool(p):
  '''neural_add_to_operand_stack_bool :'''
  operand_value = p[-1]
  operand_type = "bool"
  add_to_operand_stack(operand_value, operand_type)

def p_neural_add_to_operand_stack_id(p):
  '''neural_add_to_operand_stack_id :'''
  operand_value = p[-1]
  operand_type = gv.function_directory.get_variable_type(operand_value, gv.current_block, gv.current_class_block)
  add_to_operand_stack(operand_value, operand_type)

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
  result = p[-1]
  result_type = gv.function_directory.get_variable_type(result, gv.current_block, gv.current_class_block)
  if result_type not in Types.primitives:
    helpers.throw_error("Cannot assign input to " + result)
  quad = Quad(QuadOperations.READ, result)
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
  gv.current_sub_has_return_stmt = False

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
      file = 'test.plz'
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
