from lexer import lexer

def throw_error(error_message):
  error = 'Line %d: %s' % (lexer.lineno, error_message)
  raise Exception(error)