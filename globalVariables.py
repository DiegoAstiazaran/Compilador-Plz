from directories import FunctionDirectory

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
