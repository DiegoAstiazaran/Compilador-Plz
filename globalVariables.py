from directories import FunctionDirectory, SubroutineDirectory
from structures import Stack, QuadList, TemporalMemory, SemanticCube, MemoryManager

# Boolean for debugging parser
parse_debug = False

# Main directory with global scope, functions and classes.
function_directory = FunctionDirectory()

#
subroutine_directory = SubroutineDirectory()

# Current block of function_directory.
current_block = None

# Current block when current_block is a class.
current_class_block = None

# Current last type read in a declaration or initialization
current_last_type = None

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
current_for_operator = None

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

# Temporal memory manager
temporal_memory = TemporalMemory()

#
memory_manager = MemoryManager()

#
global_error = []

#
array_access_indices = []

# For debugging purposes
# TODO: delete
lines_read = []
