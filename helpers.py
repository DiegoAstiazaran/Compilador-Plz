from lexer import lexer

def throw_error(error_message):
  error = 'Line %d: %s' % (lexer.lineno, error_message)
  exit(error)
  # raise Exception(error)

def throw_error_no_line(error_message):
  exit(error_message)
  # raise Exception(error_message)
