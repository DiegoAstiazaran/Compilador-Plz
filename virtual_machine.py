from structures import Quad
from constants import Operators, QuadOperations, Types, Constants
from virtual_machine_memory import VirtualMachineMemoryManager
import virtual_machine_global_variables as gv
import helpers
from copy import copy

def execute_virtual_machine(quad_list, constant_memory, subroutine_directory):
  quad_pointer = 0
  memory_manager = VirtualMachineMemoryManager()
  memory_manager.add_constant_memory(constant_memory)
  items_to_read = []
  values_read = []
  while(quad_pointer < quad_list.size()):
    quad = quad_list.get(quad_pointer)
    operation = quad.get_operation()
    gv.line_number = quad.get_line_number()
    if operation == Operators.EQUAL:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      memory_manager.set_memory_value(result_address, operand)
    elif operation in Operators.binary:
      left_operand, right_operand, result_address = quad.get_items()
      left_operand = memory_manager.get_memory_value(left_operand)
      right_operand = memory_manager.get_memory_value(right_operand)
      temporal = gv.operations[operation](left_operand, right_operand)
      memory_manager.set_memory_value(result_address, temporal)
    elif operation in QuadOperations.unary or operation in Operators.unary:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      temporal = gv.operations[operation](operand)
      memory_manager.set_memory_value(result_address, temporal)
    elif operation == QuadOperations.WRITE:
      operand = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      print(operand, end = '')
    elif operation == QuadOperations.WRITE_NEW_LINE:
      print(end = '\n')
    elif operation == QuadOperations.WRITE_SPACE:
      print(end = ' ')
    elif operation == QuadOperations.READ_ITEM:
      memory_address = quad.get_items()
      items_to_read.append(memory_address)
    elif operation == QuadOperations.READ_END:
      # TODO: specify how read works in documentation
      while(len(values_read) < len(items_to_read)):
        temporal_values_read = input().split()
        values_read.extend(temporal_values_read)
      
      for value_read, memory_address in zip(values_read, items_to_read):
        type = memory_manager.get_memory_type(memory_address)
        if type == Types.INT:
          try:
            value_read = int(value_read)
          except ValueError:
            helpers.throw_error_no_line("Input value must be an integer")
        elif type == Types.FLT:
          try:
            value_read = float(value_read)
          except ValueError:
            helpers.throw_error_no_line("Input value must be a float")
        elif type == Types.BOOL and value_read not in Constants.BOOLEAN:
          helpers.throw_error_no_line("Input value must be a boolean")
        memory_manager.set_memory_value(memory_address, value_read)
      
      del values_read[:len(items_to_read)]
      items_to_read = []
    elif operation == QuadOperations.READ_LN:
      items_to_read = []      
      memory_address = quad.get_items()

      value_read = input()

      type = memory_manager.get_memory_type(memory_address)
      if type == Types.INT:
        try:
          value_read = int(value_read)
        except ValueError:
          helpers.throw_error_no_line("Input value must be an integer")
      elif type == Types.FLT:
        try:
          value_read = float(value_read)
        except ValueError:
          helpers.throw_error_no_line("Input value must be a float")
      elif type == Types.BOOL and value_read not in Constants.BOOLEAN:
        helpers.throw_error_no_line("Input value must be a boolean")
      memory_manager.set_memory_value(memory_address, value_read)
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
    elif operation == QuadOperations.VER:
      array_index_address, array_diminesion = quad.get_items()
      array_index = memory_manager.get_memory_value(array_index_address)
      if array_index < 0 or array_index >= array_diminesion:
        helpers.throw_error_no_line("Index out of bounds")
    elif operation == QuadOperations.CHECK_DIV:
      operand_address = quad.get_items()
      operand_value = memory_manager.get_memory_value(operand_address)
      if operand_value == 0:
        helpers.throw_error_no_line("Can't divide by 0")
    elif operation == QuadOperations.WRITE_ADDRESS:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      memory_manager.set_memory_value(result_address, operand, True)
    elif operation == QuadOperations.READ_ADDRESS:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand, True)
      memory_manager.set_memory_value(result_address, operand)
    elif operation == QuadOperations.ERA:
      if len(quad.get_items()) == 2:
        class_block_name, block_name = quad.get_items()
        return_temporal_address = None
      else:
        class_block_name, block_name, return_temporal_address = quad.get_items()
      subroutine_call = copy(subroutine_directory.get_subroutine(block_name, class_block_name))
      subroutine_call.append(return_temporal_address) # position 2 of array
      memory_manager.new_local_memory(subroutine_call)
    elif operation == QuadOperations.PARAM:
      param_address, param_counter = quad.get_items()
      arg_address = memory_manager.get_sub_call_arg_address(param_counter)
      param_value = memory_manager.get_memory_value(param_address)
      memory_manager.set_arg_value(arg_address, param_value)
    elif operation == QuadOperations.GOSUB:
      start = memory_manager.get_sub_call_start()
      memory_manager.set_quad_pointer(quad_pointer)
      memory_manager.set_new_local_memory()
      quad_pointer = start
      continue
    elif operation == QuadOperations.RETURN:
      return_address = quad.get_items()
      if return_address is not None:
        return_value = memory_manager.get_memory_value(return_address)
        return_temporal_address = memory_manager.get_return_temporal_address()
      
      return_position = memory_manager.get_return_position()
      memory_manager.pop_local_memory()

      if return_address is not None:
        memory_manager.set_memory_value(return_temporal_address, return_value)

      quad_pointer = return_position
    elif operation == QuadOperations.THIS_PARAM:
      type, memory_address = quad.get_items()
      this_index = Types.primitives.index(type)
      arg_address = memory_manager.get_sub_call_arg_address(this_index)
      memory_manager.set_arg_value(arg_address, memory_address)
    else:
      helpers.throw_error_no_line("Invalid quad operation!")
    quad_pointer += 1