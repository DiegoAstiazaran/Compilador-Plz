from structures import Quad
from constants import Operators, QuadOperations, Types, Constants
from structures import VirtualMachineMemoryMapManager
from virtualMachineGlobalVariables import operations
import helpers

def execute_virtual_machine(quad_list, constant_memory, subroutine_directory):
  quad_pointer = 0
  memory_manager = VirtualMachineMemoryMapManager()
  memory_manager.add_constant_memory(constant_memory)
  while(quad_pointer < quad_list.size()):
    quad = quad_list.get(quad_pointer)
    operation = quad.get_operation()   
    if operation == Operators.EQUAL:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      memory_manager.set_memory_value(result_address, operand)
    elif operation in Operators.binary:
      left_operand, right_operand, result_address = quad.get_items()
      left_operand = memory_manager.get_memory_value(left_operand)
      right_operand = memory_manager.get_memory_value(right_operand)
      temporal = operations[operation](left_operand, right_operand)
      memory_manager.set_memory_value(result_address, temporal)
    elif operation == QuadOperations.unary or operation in Operators.unary:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      temporal = operations[operation](operand)
      memory_manager.set_memory_value(result_address, temporal)
    elif operation == QuadOperations.WRITE:
      operand = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      print(operand, end = '')
    elif operation == QuadOperations.WRITE_NEW_LINE:
      print(end = '\n')
    elif operation == QuadOperations.WRITE_SPACE:
      print(end = ' ')
    elif operation == QuadOperations.READ:
      memory_address = quad.get_items()
      temporal = input()
      type = memory_manager.get_memory_type(memory_address)
      if type == Types.INT:
        try:
          temporal = int(temporal)
        except ValueError:
          helpers.throw_error_no_line("Input value must be an integer")
      elif type == Types.FLT:
        try:
          temporal = float(temporal)
        except ValueError:
          helpers.throw_error_no_line("Input value must be a float")
      elif type == Types.BOOL and temporal not in Constants.BOOLEAN:
        helpers.throw_error_no_line("Input value must be a boolean")
      memory_manager.set_memory_value(memory_address, temporal)
    elif operation == QuadOperations.GOTO:
      quad_index = quad.get_items()
      quad_pointer = quad_index
      continue
    elif operation == QuadOperations.GOTO_F or operation == QuadOperations.GOTO_T:
      condition_address, quad_index = quad.get_items()
      condition = memory_manager.get_memory_value(condition_address)
      if (operation == QuadOperations.GOTO_F and not condition) or (operation == QuadOperations.GOTO_T and condition):
        quad_pointer = quad_index
        continue
    # elif operation == QuadOperations.RETURN:
    # elif operation == QuadOperations.ERA:
    # elif operation == QuadOperations.PARAM:
    # elif operation == QuadOperations.GOSUB:
    else:
      helpers.throw_error_no_line("Invalid quad operation!")
    quad_pointer += 1