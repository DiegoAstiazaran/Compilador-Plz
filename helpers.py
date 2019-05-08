from lexer import lexer
import virtual_machine_global_variables as gv

# Error handler for compilation
def throw_error(error_message):
  error = 'Line %d: %s' % (lexer.lineno, error_message)
  exit(error)

# Error handler for virtual machine
def throw_error_no_line(error_message):
  error = 'Line %d: %s' % (gv.line_number, error_message)
  exit(error)
