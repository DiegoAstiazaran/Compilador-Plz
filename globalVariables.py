from directories import FunctionDirectory
from structures import Stack, QuadList, TemporalMemory, SemanticCube

# Boolean for debugging parser
parse_debug = False

# Main directory with global scope, functions and classes.
function_directory = FunctionDirectory()

# Current block of function_directory.
current_block = None

# Current block when current_block is a class.
current_class_block = None

# Current last type read in a declaration or initialization
current_last_type = None

# Defines if current class block is public
current_is_public = None

# Current last id declared
current_last_id = None

# Boolean to know if unary operator was parsed
read_unary_operator = False

# Semantic cube object
semantic_cube = SemanticCube()

# Stack for operators
stack_operators = Stack()

# Stack for operands, includes type and value 
stack_operands = Stack()

# List of quads
quad_list = QuadList()

# Temporal memory manager
temporal_memory = TemporalMemory()

# For debugging purposes
# TODO: delete
lines_read = []