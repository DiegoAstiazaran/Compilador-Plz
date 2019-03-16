# Define _space and _newline
_space = " "
_newline = "\n"

def program_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + _newline + p[2]
  elif len(p) == 5:
    p[0] = p[1] + _newline + p[2] + _newline + p[3] + _newline + p[4]
  else:
    raise Exception('Invalid expression for parser in p_program')

def block_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _newline + p[2]
  else:
    raise Exception('Invalid expression for parser in p_block')

def statement_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 5:
    p[0] = p[1] + _space + p[2] + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_statement')

def sub_call_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 5:
    p[0] = p[1] + _space + p[2] + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_sub_call')

def sub_call_args_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_sub_call_args')

def return_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    p[0] = p[1] + _space + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_return')

def class_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  elif len(p) == 7:
    p[0] = p[1] + _space + p[2] + _space + p[3] + p[4] + _newline + p[5] + _newline + p[6]
  else:
    raise Exception('Invalid expression for parser in p_class')

def expression_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_expression')

def mini_expression_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_mini_expression')

def exp_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  else:
    raise Exception('Invalid expression for parser in p_exp')

def term_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  else:
    raise Exception('Invalid expression for parser in p_term')

def factor_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + _space + p[2] + _space + p[3]
  else:
    raise Exception('Invalid expression for parser in p_factor')

def class_block_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 4:
    p[0] = p[1] + _newline + p[2] + _newline + p[3]
  else:
    raise Exception('Invalid expression for parser in p_class_block')

def private_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _newline + p[2]
  elif len(p) == 6:
    p[0] = p[1] + p[2] + _newline + p[3] + _newline + p[4] + _newline + p[5]
  else:
    raise Exception('Invalid expression for parser in p_private')

def public_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _newline + p[2]
  elif len(p) == 6:
    p[0] = p[1] + p[2] + _newline + p[3] + _newline + p[4] + _newline + p[5]
  else:
    raise Exception('Invalid expression for parser in p_public')

def declaration_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + _space + p[2] + p[3]
  else:
    raise Exception('Invalid expression for parser in p_declaration')

def array_size_debug(p, debug):
  if not debug:
    return
  if len(p) == 4:
    p[0] = p[1] + str(p[2]) + p[3]
  else:
    raise Exception('Invalid expression for parser in p_array_size')

def decl_init_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  else:
    raise Exception('Invalid expression for parser in p_decl_init')

def decl_init_var_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + p[3] + p[4]
  elif len(p) == 6:
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
  elif len(p) == 7:
    p[0] = p[1] + _space + p[2] + p[3] + _space + p[4] + _space + p[5] + p[6]
  else:
    raise Exception('Invalid expression for parser in p_decl_init_var')

def decl_init_dict_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_decl_init_dict')

def decl_init_obj_debug(p, debug):
  if not debug:
    return
  if len(p) == 6:
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
  else:
    raise Exception('Invalid expression for parser in p_decl_init_obj')

def assignment_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 7:
    p[0] = p[1] + _space + p[2] + p[3] + _space + p[4] + _space + p[5] + p[6]
  else:
    raise Exception('Invalid expression for parser in p_assignment')

def constructor_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + _space + p[2] + p[3]
  elif len(p) == 10:
    p[0] = p[1] + _space + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + _newline + p[8] + _newline + p[9]
  else:
    raise Exception('Invalid expression for parser in p_constructor')

def relational_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_relational')

def logical_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_logical')

def var_cte_1_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = str(p[1])
  else:
    raise Exception('Invalid expression for parser in p_var_cte_1')

def var_cte_2_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = str(p[1])
  else:
    raise Exception('Invalid expression for parser in p_var_cte_2')

def id_calls_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + _space + p[3]
  else:
    raise Exception('Invalid expression for parser in p_id_calls')

def var_cte_3_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_var_cte_3')

def cte_b_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_cte_b')

def subroutine_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 4:
    p[0] = p[1] + _space + p[2] + _space + p[3]
  elif len(p) == 11:
    p[0] = p[1] + _space + p[2] + _space + p[3] + _space + p[4] + p[5] + p[6] + p[7] + _newline + p[8] + _newline + p[9] + _newline + p[10]
  else:
    raise Exception('Invalid expression for parser in p_subroutine')

def write_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + p[2]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + _space + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_write')

def condition_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + _newline + p[3]
  elif len(p) == 5:
    p[0] = p[1] + _space + p[2] + p[3] + _space + p[4]
  else:
    raise Exception('Invalid expression for parser in p_condition')

def cycle_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_cycle')

def operator_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_operator')

def access_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 4:
    p[0] = p[1] + p[2] + p[3]
  elif len(p) == 5:
    p[0] = p[1] + _space + p[2] + _space + p[3] + p[4]
  else:
    raise Exception('Invalid expression for parser in p_access')

def when_debug(p, debug):
  if not debug:
    return
  if len(p) == 7:
    p[0] = p[1] + _space + p[2] + _space + p[3] + p[4] + _newline + p[5] + _newline + p[6]
  else:
    raise Exception('Invalid expression for parser in p_when')

def repeat_debug(p, debug):
  if not debug:
    return
  if len(p) == 7:
    p[0] = p[1] + p[2] + _newline + p[3] + _newline + p[4] + _space + p[5] + _space + p[6]
  else:
    raise Exception('Invalid expression for parser in p_repeat')

def for_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 13:
    p[0] = p[1] + _space + p[2] + _space + p[3] + _space + p[4] + _space + p[5] + _space + p[6] + p[7] + _space + p[8] + _space + p[9] + _space + p[10] + _newline + p[11] + _newline + p[12]
  else:
    raise Exception('Invalid expression for parser in p_for')

def read_debug(p, debug):
  if not debug:
    return
  if p[1] == None:
    p[0] = ""
  elif len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + _space + p[2]
  elif len(p) == 5:
    p[0] = p[1] + p[2] + _space + p[3] + _space + p[4]
  elif len(p) == 4:
    p[0] = p[1] + p[2] + _space + p[3]
  else:
    raise Exception('Invalid expression for parser in p_read')

def type_debug(p, debug):
  if not debug:
    return
  if len(p) == 2:
    p[0] = p[1]
  else:
    raise Exception('Invalid expression for parser in p_type')