from constants import Constants
import global_variables as gv      # Import global variables

# Called after CLASS_NAME in class declaration
def p_neural_class_decl(p):
  '''neural_class_decl :'''
  gv.memory_manager.reset_class()
  gv.current_class_block = p[-1]
  gv.function_directory.add_block(gv.current_class_block, Constants.CLASS_BLOCK)
  gv.subroutine_directory.add_block(gv.current_class_block)

# Called at the end of class declaration
def p_neural_class_decl_end(p):
  '''neural_class_decl_end :'''
  gv.current_class_block = None

# Called after CLASS_NAME when inheriting a class
def p_neural_class_decl_inheritance(p):
  '''neural_class_decl_inheritance :'''
  class_name = p[-1]
  gv.function_directory.check_class_exists(class_name)
  gv.function_directory.inherit_class(gv.current_class_block, class_name)
  gv.subroutine_directory.inherit_class(gv.current_class_block, class_name)

# Called after PRIVATE in public section of class declaration
def p_neural_class_decl_private(p):
  '''neural_class_decl_private :'''
  gv.current_is_public = False

# Called after PUBLIC in public section of class declaration
def p_neural_class_decl_public(p):
  '''neural_class_decl_public :'''
  gv.current_is_public = True

# 
def p_neural_is_public_none(p):
  '''neural_is_public_none :'''
  gv.current_is_public = None
