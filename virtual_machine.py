from structures import Quad
from constants import Operators, QuadOperations, Types, Constants
from virtual_machine_memory import VirtualMachineMemoryManager
import virtual_machine_global_variables as gv
import helpers
from copy import copy


# This is the main function of the virtual machine. Depending on the operation of each quad, it will decide what 
# to do. 
def execute_virtual_machine(quad_list, constant_memory, subroutine_directory):
  quad_pointer = 0
  memory_manager = VirtualMachineMemoryManager()
  memory_manager.add_constant_memory(constant_memory)
  global_addresses = subroutine_directory.get_memory_addresses_of_block(Constants.GLOBAL_BLOCK)
  items_to_read = []
  values_read = []
  while(quad_pointer < quad_list.size()):
    quad = quad_list.get(quad_pointer)
    operation = quad.get_operation()
    gv.line_number = quad.get_line_number()
    # Equal = 
    if operation == Operators.EQUAL:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      memory_manager.set_memory_value(result_address, operand)

    # <, >, <=, >=, ~=, ==, 
    elif operation in Operators.binary:
      left_operand, right_operand, result_address = quad.get_items()
      left_operand = memory_manager.get_memory_value(left_operand)
      right_operand = memory_manager.get_memory_value(right_operand)
      temporal = gv.operations[operation](left_operand, right_operand)
      if memory_manager.get_memory_type(result_address) == Types.INT:
        temporal = int(temporal)
      memory_manager.set_memory_value(result_address, temporal)

    # ~ (not)
    elif operation in QuadOperations.unary or operation in Operators.unary:
      operand, result_address = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      temporal = gv.operations[operation](operand)
      memory_manager.set_memory_value(result_address, temporal)

    # write operation
    elif operation == QuadOperations.WRITE:
      operand = quad.get_items()
      operand = memory_manager.get_memory_value(operand)
      print(operand, end = '')

    # write new line
    elif operation == QuadOperations.WRITE_NEW_LINE:
      print(end = '\n')

    # write a space
    elif operation == QuadOperations.WRITE_SPACE:
      print(end = ' ')

    # read operation
    elif operation == QuadOperations.READ_ITEM:
      memory_address = quad.get_items()
      items_to_read.append(memory_address)

    # read end to separate each read element
    elif operation == QuadOperations.READ_END:
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

    # Read a line
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

    # a normal GOTO to jump to another quad
    elif operation == QuadOperations.GOTO:
      quad_index = quad.get_items()
      quad_pointer = quad_index
      continue
    
    # GOTO True and GOTO false
    elif operation == QuadOperations.GOTO_F or operation == QuadOperations.GOTO_T:
      condition_address, quad_index = quad.get_items()
      condition = memory_manager.get_memory_value(condition_address)
      if (operation == QuadOperations.GOTO_F and not condition) or (operation == QuadOperations.GOTO_T and condition):
        quad_pointer = quad_index
        continue

    # Verify the an array access
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

    # get the memory block that will be used for a function.
    elif operation == QuadOperations.ERA:
      if len(quad.get_items()) == 2:
        class_block_name, block_name = quad.get_items()
        return_temporal_address = None
      else:
        class_block_name, block_name, return_temporal_address = quad.get_items()
      subroutine_call = copy(subroutine_directory.get_subroutine(block_name, class_block_name))
      subroutine_call.append(return_temporal_address) # position 2 of array
      memory_manager.new_local_memory(subroutine_call)

    # set the params of a function in a function call
    elif operation == QuadOperations.PARAM:
      param_address, param_counter = quad.get_items()
      arg_address = memory_manager.get_sub_call_arg_address(param_counter)
      param_value = memory_manager.get_memory_value(param_address)
      memory_manager.set_arg_value(arg_address, param_value)

    # go to the quad of the start of a function
    elif operation == QuadOperations.GOSUB:
      start = memory_manager.get_sub_call_start()
      memory_manager.set_quad_pointer(quad_pointer)
      memory_manager.set_new_local_memory()
      quad_pointer = start
      continue

    # get the return value of a function      
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
      value = memory_manager.get_memory_value(memory_address)
      memory_manager.set_arg_value(arg_address, value)
    elif operation in QuadOperations.list_methods:

      # pop method of a list
      if   operation == QuadOperations.POP:
        if len(quad.get_items()) == 3: # index
          list_address, index_address, return_address = quad.get_items()
          index = memory_manager.get_memory_value(index_address)
        elif len(quad.get_items()) == 2: # last one
          list_address, return_address = quad.get_items()
          list_size = len(memory_manager.list_get_items(list_address))
          index = list_size - 1
        pop_value = memory_manager.list_pop_node(list_address, index)
        memory_manager.set_memory_value(return_address, pop_value)

      # append method of a list
      elif operation == QuadOperations.APPEND:
        list_address, list_type, value_address = quad.get_items()
        value = memory_manager.get_memory_value(value_address)
        memory_manager.list_append_node(list_address, list_type, value, global_addresses)

      # print method of a list
      elif operation == QuadOperations.PRINT:
        list_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        print(*list_values)

      # insert method of a list
      elif operation == QuadOperations.INSERT:
        list_address, list_type, index_address, value_address = quad.get_items()
        index = memory_manager.get_memory_value(index_address)
        value = memory_manager.get_memory_value(value_address)
        memory_manager.list_insert_node(list_address, index, value, list_type, global_addresses)
      
      # remove an element of a list
      elif operation == QuadOperations.REMOVE:
        list_address, value_address = quad.get_items()
        value = memory_manager.get_memory_value(value_address)
        memory_manager.list_remove_node(list_address, value)

      # Get the index of a list
      elif operation == QuadOperations.INDEX:
        list_address, index_addreess, return_address = quad.get_items()
        index_value = memory_manager.get_memory_value(index_addreess)
        value_at_index = memory_manager.list_index_node(list_address, index_value)
        memory_manager.set_memory_value(return_address, value_at_index)

      # find an element in a list
      elif operation == QuadOperations.FIND:
        list_address, value_address, return_address = quad.get_items()
        value = memory_manager.get_memory_value(value_address)
        list_values = memory_manager.list_get_items(list_address)
        find_index = -1 if value not in list_values else list_values.index(value)
        memory_manager.set_memory_value(return_address, find_index)

      # count the elements in a list
      elif operation == QuadOperations.COUNT:
        list_address, count_address, return_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        count_value = memory_manager.get_memory_value(count_address)
        count_res = list_values.count(count_value)
        memory_manager.set_memory_value(return_address, count_res)

      # reverse a list
      elif operation == QuadOperations.REVERSE:
        list_address = quad.get_items()
        memory_manager.list_reverse(list_address)

      # get the minimum element of a list
      elif operation == QuadOperations.MIN:
        list_address, return_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        min_value = min(list_values)
        memory_manager.set_memory_value(return_address, min_value)
        print(*list_values)

      # get the maximum element of a list
      elif operation == QuadOperations.MAX:
        list_address, return_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        max_value = max(list_values)
        memory_manager.set_memory_value(return_address, max_value)
      
      # get the size of a list
      elif operation == QuadOperations.SIZE:
        list_address, return_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        list_size = len(list_values)
        memory_manager.set_memory_value(return_address, list_size)

      # check if list is empty
      elif operation == QuadOperations.EMPTY:
        list_address, return_address = quad.get_items()
        list_values = memory_manager.list_get_items(list_address)
        list_empty = len(list_values) == 0
        memory_manager.set_memory_value(return_address, list_empty)
      else:
        helpers.throw_error_no_line("Invalid list method!")
    else:
      helpers.throw_error_no_line("Invalid quad operation!")
    quad_pointer += 1
