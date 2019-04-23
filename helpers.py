from lexer import lexer
import globalVariables as gv

def throw_error(error_message):
  error = 'Line %d: %s' % (lexer.lineno, error_message)
  gv.global_error.append(error)
  # raise Exception(error)

def throw_error_no_line(error_message):
  exit(error_message)
  # gv.global_error.append(error_message)
  # raise Exception(error_message)
