from constants import Constants
from function_directory import FunctionDirectory
from subroutine_directory import SubroutineDirectory
from structures import Stack, QuadList
from semantic_cube import SemanticCube
from parser_memory import ParserMemoryManager

# Main directory with global scope, functions and classes.
function_directory = FunctionDirectory()

# Directory with subrotine headers
subroutine_directory = SubroutineDirectory()

# Current block of function_directory
# "Global" si no esta en un metodo
current_block = Constants.GLOBAL_BLOCK

# Current block when current_block is a class.
current_class_block = None

# Current last type read in a declaration or initialization
current_last_type = None

# Current type of param
current_param_type = None

# Defines if current class block is public
current_is_public = None

# Current last id declared
current_last_id = None

# Boolean to know if unary operator was parsed
read_unary_operator = False

# Boolean to know if current return statement returns a value
current_return_has_value = False

# Boolean to know if current subroutine has a return statement
current_sub_has_return_stmt = False

# Boolean to know if there is an else in current condition_p
current_condition_has_else = False

# Boolean to know if the condition has reached the end
condition_end = False

# Operator value for current for cycle
stack_for_operators = Stack()

#
sub_call_first_id = None

#
sub_call_second_id = None

# Semantic cube object
semantic_cube = SemanticCube()

# Stack for operators
stack_operators = Stack()

# Stack for operands, includes type and value
stack_operands = Stack()

# Stack for jumps for GoTo
stack_jumps = Stack()

# Stack for suboroutine calls
stack_sub_calls = Stack()

# List of quads
quad_list = QuadList()

# The main memory manager for runtime
memory_manager = ParserMemoryManager()

# Keeps the indexes that will be accessed on an array
array_access_indices = []

# Keeps the initial values of an array initialization
array_init_values = None

# Keeps the initial values of a list initialization
list_init_values = []

# Keeps the current object being referenced
current_this = False

# Checks if the print has a newline
print_new_line = None

# keeps if current variable is a list
current_is_list = False
