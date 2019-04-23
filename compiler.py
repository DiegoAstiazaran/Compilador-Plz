import globalVariables as gv
from parser import execute_parser
from virtual_machine import execute_virtual_machine

def compiler(input):
  quad_list, constant_memory, subroutine_directory = execute_parser(input)
  if len(gv.global_error) == 0:
    execute_virtual_machine(quad_list, constant_memory, subroutine_directory)
  return gv.global_error