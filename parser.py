# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens, lexer   # Import tokens and lexer defined in lexer
import global_variables as gv      # Import global variables
from neural_points import *

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
             | neural_new_goto class neural_fill_goto
             | neural_new_goto subroutine neural_fill_goto
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
  sub_call : ID neural_sub_call_first_id sub_call_p neural_sub_call sub_call_args neural_sub_call_end_no_return_value DOT
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
  expression : neural_expression_start mini_expression neural_check_operator_stack_logical expression_p neural_expression_end
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
  factor : L_PAREN expression R_PAREN
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
  declaration_pp : array_size declaration_ppp neural_array_decl_end
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
                  | decl_init_var_pp neural_array_decl_end
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
  decl_init_obj : CLASS_NAME ID neural_var_decl_id neural_constructor_call sub_call_args neural_sub_call_end_no_return_value
  '''
  # TODO: Put neural_add_to_operator_stack back after EQUAL

def p_assignment(p):
  '''
  assignment : id_attr_access EQUAL neural_add_to_operator_stack expression neural_check_operator_stack_equal DOT
  '''

def p_id_attr_access(p):
  '''
  id_attr_access : ID neural_add_to_operand_stack_id id_attr_access_obj id_attr_access_access neural_restart_object
  id_attr_access_obj : AT ID neural_at_attribute
                     | empty
  id_attr_access_access : access
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
  id_calls_p : neural_add_subcall_first_id_to_stack access
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
  access : L_SQ_BRACKET expression R_SQ_BRACKET neural_array_access_first access_p neural_array_access_end
  access_p : L_SQ_BRACKET expression R_SQ_BRACKET neural_array_access_second
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

# You can read an id or attribute of id(obj) with a possible array access
def p_read(p):
  '''
  read : READ COLON read_list END
  read_list : read_p read_list_p
  read_list_p : COMMA read_list
              | empty
  read_p : id_attr_access neural_read_stmt
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
  helpers.throw_error('Syntax error in input!')

# Execution of parser with a filename
def execute_parser(input):
  # Build the parser
  parser = yacc.yacc()
  parser.parse(input)
  print(gv.quad_list)
  # gv.quad_list.print_with_number()
  gv.subroutine_directory.fix_for_virtual_machine()
  return gv.quad_list, gv.memory_manager.get_constant_map(), gv.subroutine_directory
