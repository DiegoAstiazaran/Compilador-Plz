from parser import execute_parser
from virtual_machine import execute_virtual_machine

quad_list = execute_parser()
execute_virtual_machine(quad_list)
