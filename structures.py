from constants import Constants
import helpers
from lexer import lexer

# Item for operands inserted to stack
class OperandItem:
  def __init__(self, operand_value, operand_type, block_name = None, class_name = None):
    self._item = (operand_value, operand_type, block_name, class_name)

  def __str__(self):
    return str(self._item)

  def __repr__(self):
    return str(self._item)

  def get_value(self):
    return self._item[0]

  def get_type(self):
    return self._item[1]
  
  def get_block_name(self):
    return self._item[2]
  
  def get_class_name(self):
    return self._item[3]

# Implementantion of stack
class Stack:
  def __init__(self):
    self._stack = []

  def __str__(self):
    return str(self._stack)

  def push(self, value):
    self._stack.append(value)

  # Pops and returns element
  def pop(self):
    top = self.top()
    self._stack.pop()
    return top

  def top(self):
    return self._stack[-1]

  def empty(self):
    return not self._stack

# List for quads
class QuadList:
  def __init__(self):
    self._quad_list = []

  def __str__(self):
    return '[\n' + ',\n'.join('{}'.format(item) for item in self._quad_list) + '\n]'

  def next(self):
    return len(self._quad_list)

  def size(self):
    return len(self._quad_list)

  def add(self, quad):
    self._quad_list.append(quad)

  def erase(self, index):
    self._quad_list.pop(index)

  def add_element_to_quad(self, index, element):
    self._quad_list[index].add_element(element)
  
  def get(self, index):
    return self._quad_list[index]

  def print_with_number(self):
    index = 0
    for item in self._quad_list:
      print('#{}\t{}'.format(index, item))
      index += 1
  
# Quad for intermediate code
class Quad:
  def __init__(self, instruction, first = None, second = None, third = None):
    self._lineno = lexer.lineno
    if instruction is None:
      helpers.throw_error("Quad operator must be different from None")
    self._quad = [instruction]
    if first is not None:
      self._quad.append(first)
    if second is not None:
      self._quad.append(second)
    if third is not None:
      self._quad.append(third)

  def __repr__(self):
    return ' '.join(str(i) for i in filter(None.__ne__, self._quad))

  def add_element(self, element):
    self._quad.append(element)
  
  def get_operation(self):
    return self._quad[0]
  
  def get_line_number(self):
    return self._lineno

  def get_items(self):
    if len(self._quad) > 2:
      return tuple(self._quad[1:])
    if len(self._quad) == 2:
      return self._quad[1]
    else:
      return None
  
class SubCall:
  def __init__(self, sub_name, block_name, object_name):
    # block name is the class
    if block_name == None:
      block_name = Constants.GLOBAL_BLOCK
    self._object_name = object_name
    self._sub_name = sub_name
    self._block_name = block_name
    self._param_count = 0
  
  def get_sub_name_block_name(self):
    return self._sub_name, self._block_name
  
  def get_param_count(self):
    return self._param_count
  
  def add_param_count(self):
    self._param_count += 1
  
  def get_sub_name(self):
    return self._sub_name

  def get_block_name(self):
    return self._block_name

  def is_class_method(self):
    return self._object_name is not None

  def add_return_temporal_address(self, memory_address):
    self._return_temporal_address = memory_address
  
  def get_return_temporal_address(self):
    return self._return_temporal_address
