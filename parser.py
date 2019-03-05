# Erik Torres A01196362
# Diego Astiazaran A01243969

import ply.yacc as yacc # Import yacc module

from lexer import tokens # Import tokens defined in lexer

# Define space and newline
space = " "
newline = "\n"

def p_program(p):
  '''
  program : program_p program_class program_subroutine block
  program_p : initialization
            | declaration 
            | assignment
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
    p[0] = p[1] + newline + p[2] + newline + p[3] + newline + p[4] + newline + p[5]
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
            | conditional
            | write
            | cycle
            | subcall
            | return
            | attr_call
  '''
  if len(p) == 2:
      p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_statement')

def p_return(p):
  '''
  return : RETURN return_expression DOT
  return_expression : expression
                    | empty
  '''
  if p[0] == None:
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
  if p[0] == None:
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
  if p[0] == None:
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
  if p[0] == None:
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
  if p[0] == None:
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
         | factor_p var_cte_4
  factor_p : PLUS
           | MINUS
           | empty
  '''
  if p[0] == None:
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
  class_block : class_block_private class_block_public
  class_block_private : private
                      | empty
   class_block_public : public
                      | empty
  '''
  if p[0] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  else:
    raise Exception('Invalid expression for parser in p_class_block')

def p_private(p):
  '''
  private : private_declaration private_subroutine
  private_declaration : PRIVATE declaration private_declaration
                      | empty
  private_subroutine : PRIVATE subroutine private_subroutine
                     | empty
  '''
  if p[0] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + newline + p[3]
  else:
    raise Exception('Invalid expression for parser in p_private')

def p_public(p):
  '''
  public : public_declaration public_subroutine
  public_declaration : PUBLIC declaration public_declaration
                     | empty
  public_subroutine : PUBLIC subroutine public_subroutine
                    | empty
  '''
  if p[0] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + newline + p[2]
  elif len(p) == 4:
    p[0] = p[1] + space + p[2] + newline + p[3]
  else:
    raise Exception('Invalid expression for parser in p_public')
  
# def p_declaration(p):
#   '''
#   declaration : declaration_p DOT
#   declaration_p : dec_var
#                 | dec_arr
#                 | dec_mat
#                 | dec_dict
#   '''
#   if len(p) == 2:
#     p[0] = p[1]
#   elif len(p) == 3:
#     p[0] = p[1] + p[2]
#   else:
#     raise Exception('Invalid expression for parser in p_declaration')

# def p_dec_var(p):
#   '''
#   dec_var : type ID
#   '''
#   if len(p) == 3:
#     p[0] = p[1] + space + p[2]
#   else:
#     raise Exception('Invalid expression for parser in p_dec_var')

# def p_dec_arr(p):
#   '''
#   dec_arr : type ID L_PAREN CTE_I R_PAREN
#   '''
#   if len(p) == 6:
#     p[0] = p[1] + space + p[2] + p[3] + p[4] + p[5]
#   else:
#     raise Exception('Invalid expression for parser in dec_arr')

# def p_dec_mat(p):
#   '''
#   dec_mat : type ID L_PAREN CTE_I R_PAREN L_PAREN CTE_I R_PAREN
#   '''
#   if len(p) == 9:
#     p[0] = p[1] + space + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]
#   else:
#     raise Exception('Invalid expression for parser in dec_mat')

# def p_dec_dict(p):
#   '''
#   dec_dict : DICT ID
#   '''
#   if len(p) == 3:
#     p[0] = p[1] + space + p[2]
#   else:
#     raise Exception('Invalid expression for parser in dec_dict')

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
  var_cte_2 : var_cte_1
            | CTE_F
            | CTE_S
            | CTE_B
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_2')

def p_var_cte_3(p):
  '''
  var_cte_3 : var_cte_2
            | access
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_3')

def p_var_cte_4(p):
  '''
  var_cte_4 : var_cte_3
            | sub_call
            | attr_call
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_4')

def p_var_cte_5(p):
  '''
  var_cte_5 : var_cte_1
            | CTE_S
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_5')

def p_cte_b(p):
  '''
  cte_b : TRUE
        | FALSE
  '''
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_cte_b')

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