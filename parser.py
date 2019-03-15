# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens # Import tokens defined in lexer
from parserDebug import * # Import functions to debug parser

parse_debug = False # Boolean for debugging parser

# Sets main grammar rule
start = 'program'

# Functions for all grammar rules
# Function name indicates what each of them are used for

def p_program(p):
  '''
  program : program_p program_class program_subroutine block
  program_p : program_pp program_p
            | empty
  program_pp : initialization
             | declaration
  program_class : class program_class
                | empty
  program_subroutine : subroutine program_subroutine
                     | empty
  '''
  program_debug(p, parse_debug)

def p_block(p):
  '''
  block : statement block
        | empty
  '''
  block_debug(p, parse_debug)

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
  statement_debug(p, parse_debug)

def p_sub_call(p):
  '''
  sub_call : ID sub_call_p sub_call_args DOT
  sub_call_p : MONEY ID
             | empty
  '''
  sub_call_debug(p, parse_debug)

def p_sub_call_args(p):
  '''
  sub_call_args : L_PAREN sub_call_args_p R_PAREN
  sub_call_args_p : expression sub_call_args_pp
                  | empty
  sub_call_args_pp : COMMA sub_call_args_p
                  | empty
  '''
  sub_call_args_debug(p, parse_debug)

def p_return(p):
  '''
  return : RETURN return_expression DOT
  return_expression : expression
                    | empty
  '''
  return_debug(p, parse_debug)

def p_class(p):
  '''
  class : CLASS CLASS_NAME class_p COLON class_block END
  class_p : UNDER CLASS_NAME
          | empty
  '''
  class_debug(p, parse_debug)

def p_expression(p):
  '''
  expression : mini_expression expression_p
  expression_p : logical expression
               | empty
  '''
  expression_debug(p, parse_debug)

def p_mini_expression(p):
  '''
  mini_expression : exp mini_expression_p
  mini_expression_p : relational exp
                    | empty
  '''
  mini_expression_debug(p, parse_debug)

def p_exp(p):
  '''
  exp : term exp_p
  exp_p : exp_pp exp
        | empty
  exp_pp : PLUS
         | MINUS
  '''
  exp_debug(p, parse_debug)

def p_term(p):
  '''
  term : factor term_p
  term_p : term_pp term
         | empty
  term_pp : MULTIPLY
          | DIVIDE
  '''
  term_debug(p, parse_debug)

def p_factor(p):
  '''
  factor : L_PAREN expression R_PAREN
         | factor_p var_cte_2
  factor_p : PLUS
           | MINUS
           | NOT
           | NOT_OP
           | empty
  '''
  factor_debug(p, parse_debug)

def p_class_block(p):
  '''
  class_block : constructor class_block_private class_block_public
  class_block_private : private
                      | empty
  class_block_public : public
                     | empty
  '''
  class_block_debug(p, parse_debug)

def p_private(p):
  '''
  private : PRIVATE COLON private_declaration private_sub END
  private_declaration : declaration private_declaration
                      | empty
  private_sub : subroutine private_sub
              | empty
  '''
  private_debug(p, parse_debug)

def p_public(p):
  '''
  public : PUBLIC COLON public_declaration public_sub END
  public_declaration : declaration public_declaration
                     | empty
  public_sub : subroutine public_sub
             | empty
  '''
  public_debug(p, parse_debug)

def p_declaration(p):
  '''
  declaration : declaration_p DOT
  declaration_p : type ID declaration_pp
                | DICT ID
  declaration_pp : array_size declaration_ppp
                 | empty
  declaration_ppp : array_size
                  | empty
  '''
  declaration_debug(p, parse_debug)

def p_array_size(p):
  '''
  array_size : L_PAREN CTE_I R_PAREN
  '''
  array_size_debug(p, parse_debug)

def p_decl_init(p):
  '''
  decl_init : decl_init_p DOT
  decl_init_p : decl_init_var
              | decl_init_dict
              | decl_init_obj
  '''
  decl_init_debug(p, parse_debug)

def p_decl_init_var(p):
  '''
  decl_init_var : type ID decl_init_var_p
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
  decl_init_var_debug(p, parse_debug)
    
def p_decl_init_dict(p):
  '''
  decl_init_dict : DICT ID dict_init_dict_p
  dict_init_dict_p : EQUAL L_BRACKET initialization_dict R_BRACKET
                   | empty
  initialization_dict : var_cte_3 COLON expression initialization_dict_p
  initialization_dict_p : COMMA initialization_dict
                        | empty
  '''
  decl_init_dict_debug(p, parse_debug)

def p_decl_init_obj(arg):
  '''
  decl_init_obj : CLASS_NAME ID EQUAL CLASS_NAME sub_call_args
  '''
  decl_init_obj_debug(p, parse_debug)

def p_assignment(p):
  '''
  assignment : ID assignment_obj assignment_access EQUAL expression DOT
  assignment_obj : MONEY ID
                 | empty
  assignment_access : access
                    | empty
  '''
  assignment_debug(p, parse_debug)

def p_constructor(p):
  '''
  constructor : SUB CLASS_NAME L_PAREN constructor_params R_PAREN COLON constructor_p block END
  constructor_params : type ID constructor_params_p
                     | empty
  constructor_params_p : COMMA constructor_params
                       | empty
  constructor_p : constructor_pp constructor_p
                | empty
  constructor_pp : initialization
                 | declaration
  '''
  constructor_debug(p, parse_debug)

def p_relational(p):
  '''
  relational : L_THAN
             | G_THAN
             | NOT_EQ
             | L_THAN_EQ
             | G_THAN_EQ
             | EQ_TO
             | GT
             | LT
             | GTE
             | LTE
             | EQ
             | NEQ
  '''
  relational_debug(p, parse_debug)

def p_logical(p):
  '''
  logical : OR_OP
          | AND_OP
          | OR
          | AND
  '''
  logical_debug(p, parse_debug)

def p_var_cte_1(p):
  '''
  var_cte_1 : ID
            | CTE_I
  '''
  var_cte_1_debug(p, parse_debug)

def p_var_cte_2(p):
  '''
  var_cte_2 : CTE_I
            | CTE_F
            | CTE_STR
            | cte_b
            | id_calls
  '''
  var_cte_2_debug(p, parse_debug)

def p_id_calls(p):
  '''
  id_calls : ID id_calls_obj id_calls_p
  id_calls_obj : MONEY ID
               | empty
  id_calls_p : access
             | sub_call_args
             | empty
  '''
  id_calls_debug(p, parse_debug)

def p_var_cte_3(p):
  '''
  var_cte_3 : var_cte_1
            | CTE_STR
  '''
  var_cte_3_debug(p, parse_debug)

def p_cte_b(p):
  '''
  cte_b : TRUE
        | FALSE
  '''
  cte_b_debug(p, parse_debug)

def p_subroutine(p):
  '''
  subroutine : SUB subroutine_return_type ID L_PAREN subroutine_params R_PAREN COLON subroutine_p block END
  subroutine_return_type : type
                         | VOID
  subroutine_params : type ID subroutine_params_p
                    | empty
  subroutine_params_p : COMMA subroutine_params
                    | empty
  subroutine_p : subroutine_pp subroutine_ppp
               | empty
  subroutine_pp : initialization
                | declaration
  subroutine_ppp : subroutine_p
  '''
  subroutine_debug(p, parse_debug)

def p_write(p):
  '''
  write : PRINT COLON write_p END
  write_p : expression write_pp
  write_pp : COMMA write_p
           | empty
  '''
  write_debug(p, parse_debug)

def p_condition(p):
  '''
  condition : IF condition_p condition_ppp END
  condition_p : expression COLON block condition_pp
  condition_pp : ELSIF condition_p
               | empty
  condition_ppp : ELSE COLON block
                | empty
  '''
  condition_debug(p, parse_debug)

def p_cycle(p):
  '''
  cycle : when
        | repeat
        | for
  '''
  cycle_debug(p, parse_debug)

def p_operator(p):
  '''
  operator : PLUS
           | MINUS
           | MULTIPLY
           | DIVIDE
  '''
  operator_debug(p, parse_debug)

def p_access(p):
  '''
  access : L_SQ_BRACKET expression R_SQ_BRACKET access_p
  access_p : L_SQ_BRACKET expression R_SQ_BRACKET
           | empty
  '''
  access_debug(p, parse_debug)

def p_when(p):
  '''
  when : WHEN expression REPEAT COLON block END
  '''
  when_debug(p, parse_debug)

def p_repeat(p):
  '''
  repeat : REPEAT COLON block WHILE expression END
  '''
  repeat_debug(p, parse_debug)

def p_for(p):
  '''
  for : FOR ID FROM for_p BY for_operator var_cte_1 WHILE expression COLON block END
  for_p : id_calls
        | CTE_I
  for_operator : operator
               | empty
  '''
  for_debug(p, parse_debug)

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
  read_debug(p, parse_debug)

def p_type(p):
  '''
  type : INT
       | FLT
       | BOOL
       | STR
  '''
  type_debug(p, parse_debug)

def p_empty(p):
  'empty :'
  pass

# Error rule for syntax errors
def p_error(p):
  print("Syntax error in input!")

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
