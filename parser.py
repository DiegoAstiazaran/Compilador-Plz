# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens, lexer   # Import tokens and lexer defined in lexer
from parserDebug import *         # Import functions to debug parser
import globalVariables as gv      # Import global variables
from constants import *           # Import all constants
from structures import OperandPair, Quad, Operators  # Import OperandPair and Quad class
import helpers                    # Import helpers

# Sets main grammar rule
start = 'program'

# Functions for all grammar rules
# Function name indicates what each of them are used for

def p_program(p):
  '''
  program : neural_global_block program_p program_class program_subroutine block
  program_p : decl_init program_p
            | empty
  program_class : class program_class
                | empty
  program_subroutine : subroutine program_subroutine
                     | empty
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
  return : RETURN return_expression DOT
  return_expression : expression
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
  expression : mini_expression expression_p
  expression_p : logical expression
               | empty
  '''
  expression_debug(p, gv.parse_debug)

def p_mini_expression(p):
  '''
  mini_expression : exp mini_expression_p
  mini_expression_p : relational exp
                    | empty
  '''
  mini_expression_debug(p, gv.parse_debug)

def p_exp(p):
  '''
  exp : term exp_p
  exp_p : exp_pp exp
        | empty
  exp_pp : PLUS   neural_add_to_operator_stack
         | MINUS  neural_add_to_operator_stack
  '''
  exp_debug(p, gv.parse_debug)

def p_term(p):
  '''
  term : factor term_p
  term_p : term_pp term
         | empty
  term_pp : MULTIPLY  neural_add_to_operator_stack
          | DIVIDE    neural_add_to_operator_stack
  '''
  term_debug(p, gv.parse_debug)

def p_factor(p):
  '''
  factor : L_PAREN neural_operator_stack_push_false expression R_PAREN neural_operator_stack_pop_false
         | factor_p var_cte_2
  factor_p : PLUS   neural_read_unary_operator neural_add_to_operator_stack
           | MINUS  neural_read_unary_operator neural_add_to_operator_stack
           | NOT    neural_read_unary_operator neural_add_to_operator_stack
           | NOT_OP neural_read_unary_operator neural_add_to_operator_stack
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
  declaration : declaration_p DOT
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
  decl_init : decl_init_p DOT
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
  decl_init_var_var : EQUAL expression
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
  decl_init_dict_debug(p, gv.parse_debug)

def p_decl_init_obj(p):
  '''
  decl_init_obj : CLASS_NAME ID neural_var_decl_id EQUAL CLASS_NAME sub_call_args
  '''
  decl_init_obj_debug(p, gv.parse_debug)

def p_assignment(p):
  '''
  assignment : ID assignment_obj assignment_access EQUAL expression DOT
  assignment_obj : MONEY ID
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
  id_calls : ID neural_add_to_operand_stack_id id_calls_obj id_calls_p
  id_calls_obj : MONEY ID
               | empty
  id_calls_p : access
             | sub_call_args
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
  subroutine : SUB subroutine_return_type ID neural_sub_decl_id L_PAREN subroutine_params R_PAREN COLON subroutine_p block END neural_global_block
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
  write : PRINT COLON write_p END
  write_p : expression write_pp
  write_pp : COMMA write_p
           | empty
  '''
  write_debug(p, gv.parse_debug)

def p_condition(p):
  '''
  condition : IF condition_p condition_ppp END
  condition_p : expression COLON block condition_pp
  condition_pp : ELSIF condition_p
               | empty
  condition_ppp : ELSE COLON block
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
  when : WHEN expression REPEAT COLON block END
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
  read_p : ID read_obj read_access
  read_obj : MONEY ID
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
  gv.current_block = GLOBAL_BLOCK

# Called after CLASS_NAME in class declaration
def p_neural_class_decl(p):
  '''neural_class_decl :'''
  gv.current_class_block = p[-1]
  gv.function_directory.add_block(gv.current_class_block, CLASS_BLOCK)

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
    gv.current_last_type = CONSTRUCTOR_BLOCK
  gv.function_directory.add_block(gv.current_block, gv.current_last_type, gv.current_is_public, gv.current_class_block)
  gv.current_last_type = None

#################################################
#######  Expression Quad Constructions  #########
#################################################

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

# Build the parser
parser = yacc.yacc()

# Execution of parser with a filename
while True:
  try:
      file = input('Filename: ')
      with open(file, 'r') as myfile:
          s = myfile.read()
  except EOFError:
      break
  if not file: continue
  result = parser.parse(s)
  print(result)
  # gv.function_directory.output()
