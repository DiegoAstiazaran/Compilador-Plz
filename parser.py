# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens # Import tokens defined in lexer

# Define space and newline
space = " "
newline = "\n"

start = 'factor'

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
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  elif len(p) == 5:
    p[0] = p[1] + newline + p[2] + newline + p[3] + newline + p[4]
  else:
    raise Exception('Invalid expression for parser in p_program')

def p_block(p):
  '''
  block : statement block_statement
  block_statement : statement block_statement
                  | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  else:
    raise Exception('Invalid expression for parser in p_block')

def p_statement(p):
  '''
  statement : read
            | assignment
            | condition
            | write
            | cycle
            | statement_sub_call DOT
            | return
  statement_sub_call : ID statement_sub_call_p sub_call_args
  statement_sub_call_p : MONEY ID
                       | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_statement')

def p_sub_call_args(p):
  '''
  sub_call_args : L_PAREN sub_call_args_p R_PAREN
  sub_call_args_p : expression sub_call_args_pp
                  | empty
  sub_call_args_pp : COMMA sub_call_args_p
                  | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_sub_call_args')

def p_return(p):
  '''
  return : RETURN return_expression DOT
  return_expression : expression
                    | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_return')

def p_class(p):
  '''
  class : CLASS CLASS_NAME class_p COLON class_block END
  class_p : UNDER CLASS_NAME
          | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  elif len(p) == 7:
    p[0] = p[1] + space + p[2] + space + p[3] + p[4] + newline + p[5] + newline + p[6]
  else:
    raise Exception('Invalid expression for parser in p_class')

def p_expression(p):
  '''
  expression : exp expression_p
  expression_p : expression_pp exp
               | empty
  expression_pp : relational
                | logical
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_expression')

def p_exp(p):
  '''
  exp : term exp_p
  exp_p : exp_pp exp
        | empty
  exp_pp : PLUS
         | MINUS
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_exp')

def p_term(p):
  '''
  term : factor term_p
  term_p : term_pp term
         | empty
  term_pp : MULTIPLY
          | DIVIDE
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_term')

def p_factor(p):
  '''
  factor : L_PAREN expression R_PAREN
         | factor_p var_cte_2
  factor_p : PLUS
           | MINUS
           | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + space + p[3]
  else:
    raise Exception('Invalid expression for parser in p_factor')

def p_class_block(p):
  '''
  class_block : constructor private public
  '''
  if len(p) == 4:
    p[0] = p[1] + newline + p[2] + newline + p[3]
  else:
    raise Exception('Invalid expression for parser in p_class_block')

def p_private(p):
  '''
  private : PRIVATE COLON private_declaration private_sub END
  private_declaration : declaration private_declaration
                      | empty
  private_sub : subroutine private_sub
              | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  elif len(p) == 6:
    p[0] = p[1] + p[2] + newline + p[3] + newline + p[4] + newline + p[5]
  else:
    raise Exception('Invalid expression for parser in p_private')

def p_public(p):
  '''
  public : PUBLIC COLON public_declaration public_sub END
  public_declaration : declaration public_declaration
                      | empty
  public_sub : subroutine public_sub
              | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  elif len(p) == 6:
    p[0] = p[1] + p[2] + newline + p[3] + newline + p[4] + newline + p[5]
  else:
    raise Exception('Invalid expression for parser in p_public')

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
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_declaration')

def p_array_size(p):
  '''
  array_size : L_PAREN CTE_I R_PAREN
  '''
  if len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_array_size')

def p_initialization(p):
  '''
  initialization : initialization_p DOT
  initialization_p : type ID initialization_array
                   | DICT ID EQUAL L_BRACKET initialization_dict R_BRACKET
                   | CLASS_NAME ID EQUAL CLASS_NAME L_PAREN initialization_const R_PAREN
  initialization_array : array_size initialization_array_p
  initialization_array_p : EQUAL L_BRACKET array_content R_BRACKET
                         | array_size EQUAL L_BRACKET matrix_content R_BRACKET
  array_content : expression array_content_p
  array_content_p : COMMA array_content
                  | empty
  matrix_content : L_BRACKET array_content R_BRACKET matrix_content_p
  matrix_content_p : COMMA matrix_content
                   | empty
  initialization_dict : var_cte_3 COLON expression initialization_dict_p
  initialization_dict_p : COMMA initialization_dict
                   | empty
  initialization_const : expression initialization_const_p
  initialization_const_p : COMMA initialization_const
                         | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + space + p[2] + p[3] + p[4]
  elif len(p) == 6:
    p[0] = p[1] + space + p[2] + space + p[3] + p[4] + p[5]
  elif len(p) == 7:
    p[0] = p[1] + space + p[2] + space + p[3] + space + p[4] + space + p[5] + space + p[6]
  elif len(p) == 8:
    p[0] = p[1] + space + p[2] + space + p[3] + space + p[4] + p[5] + p[6] + p[7]
  else:
    raise Exception('Invalid expression for parser in p_initialization')

def p_assignment(p):
  '''
  assignment : assignment_p DOT
  assignment_p : assig_var
               | assig_cont
               | assig_attr
  '''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  else:
    raise Exception('Invalid expression for parser in p_assignment')

def p_assig_var(p):
  '''
  assig_var : ID EQUAL expression
  '''
  if len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_assig_var')

def p_assig_cont(p):
  '''
  assig_cont : ID access EQUAL expression
  '''
  if len(p) == 5:
    p[0] = p[1] + space + p[2] + space + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_assig_cont')

def p_assig_attr(p):
  '''
  assig_attr : ID MONEY ID assig_attr_p EQUAL expression
  assig_attr_p : access
                | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 7:
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
  elif len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_assig_attr')

def p_constructor(p):
  '''
  constructor : SUB CLASS_NAME L_PAREN constructor_params R_PAREN COLON constructor_p block END
  constructor_params : type ID constructor_params_p
  constructor_params_p : COMMA constructor_params
                       | empty
  constructor_p : constructor_pp constructor_ppp
                | empty
  constructor_pp : initialization
                 | declaration
  constructor_ppp : constructor_p
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  elif len(p) == 10:
    p[0] = p[1] + space + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + newline + p[8] + newline + p[9]
  else:
    raise Exception('Invalid expression for parser in p_constructor')

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
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_relational')

def p_logical(p):
  '''
  logical : OR_OP
          | AND_OP
          | NOT_OP
          | OR
          | AND
          | NOT
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_logical')

def p_var_cte_1(p):
  '''
  var_cte_1 : ID
            | CTE_I
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_1')

def p_var_cte_2(p):
  '''
  var_cte_2 : CTE_I
            | CTE_F
            | CTE_STR
            | cte_b
            | id_calls
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_2')

def p_id_calls(p):
  '''
  id_calls : ID id_calls_p
  id_calls_p : sub_call_args
             | MONEY ID id_calls_pp
             | empty
  id_calls_pp : access
              | sub_call_args
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + space + p[3]
  else:
    raise Exception('Invalid expression for parser in p_id_calls')

def p_var_cte_3(p):
  '''
  var_cte_3 : var_cte_1
            | CTE_STR
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_3')

def p_cte_b(p):
  '''
  cte_b : TRUE
        | FALSE
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_cte_b')

def p_subroutine(p):
  '''
  subroutine : SUB subroutine_return_type ID L_PAREN subroutine_params R_PAREN COLON subroutine_p block END
  subroutine_return_type : type
                         | VOID
  subroutine_params : type ID subroutine_params_p
  subroutine_params_p : COMMA subroutine_params
                    | empty
  subroutine_p : subroutine_pp subroutine_ppp
               | empty
  subroutine_pp : initialization
                | declaration
  subroutine_ppp : subroutine_p
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + space + p[3]
  elif len(p) == 11:
    p[0] = p[1] + space + p[2] + space + p[3] + space + p[4] + p[5] + p[6] + p[7] + newline + p[8] + newline + p[9] + newline + p[10]
  else:
    raise Exception('Invalid expression for parser in p_subroutine')

def p_write(p):
  '''
  write : PRINT COLON write_p END
  write_p : expression write_pp
  write_pp : COMMA write_p
           | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + space + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_write')

def p_condition(p):
  '''
  condition : IF condition_p condition_ppp END
  condition_p : expression COLON block condition_pp
  condition_pp : ELSIF condition_p
               | empty
  condition_ppp : ELSE block
                | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  elif len(p) == 5:
    p[0] = p[1] + space + p[2] + p[3] + space + p[4]
  else:
    raise Exception('Invalid expression for parser in p_condition')

def p_cycle(p):
  '''
  cycle : when
        | repeat
        | for
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_cycle')

def p_operator(p):
  '''
  operator : PLUS
           | MINUS
           | MULTIPLY
           | DIVIDE
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_operator')

def p_access(p):
  '''
  access : L_SQ_BRACKET expression R_SQ_BRACKET access_p
  access_p : L_SQ_BRACKET expression R_SQ_BRACKET
           | empty
  '''
  if len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + space + p[2] + space + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_access')

def p_when(p):
  '''
  when : WHEN expression REPEAT COLON block END
  '''
  if len(p) == 7:
    p[0] = p[1] + space + p[2] + space + p[3] + p[4] + newline + p[5] + newline + p[6]
  else:
    raise Exception('Invalid expression for parser in p_when')

def p_repeat(p):
  '''
  repeat : REPEAT COLON block WHILE expression END
  '''
  if len(p) == 7:
    p[0] = p[1] + p[2] + newline + p[3] + newline + p[4] + space + p[5] + space + p[6]
  else:
    raise Exception('Invalid expression for parser in p_repeat')

def p_for(p):
  '''
  for : FOR ID FROM id_calls BY for_operator var_cte_1 WHILE expression COLON block END
  for_operator : operator
               | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 13:
    p[0] = p[1] + space + p[2] + space + p[3] + space + p[4] + space + p[5] + space + p[6] + p[7] + space + p[8] + space + p[9] + space + p[10] + newline + p[11] + newline + p[12]
  else:
    raise Exception('Invalid expression for parser in p_for')

def p_read(p):
  '''
  read : READ COLON read_p END
  read_p : ID read_pp read_ppp
  read_pp : access
          | empty
  read_ppp : COMMA read_p
           | empty
  '''
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + space + p[3] + space + p[4]
  else:
    raise Exception('Invalid expression for parser in p_read')

def p_type(p):
  '''
  type : INT
       | FLT
       | BOOL
       | STR
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_type')

def p_empty(p):
  'empty :'
  pass

# Error rule for syntax errors
def p_error(p):
  print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
  try:
    s = input('input > ')
  except EOFError:
    break
  if not s: continue
  result = parser.parse(s)
  print(result)
