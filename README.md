# Compilador-Plz


###Project Purpose

The purpose of this project is to learn the basic functionalities of a programming language compiler. To understand the processes that happen from lexical analysis to runtime. To understand and build a virtual machine that can execute the code.

###Language main objective

The category we chose for this language is number 3: A basic object oriented language, that provides mechanisms to define classes, attributes, methods, and single inheritance and the basic elements of a programming language such as loops, statements, expressions, input and output and basic data structures.

###Reserved Words

|               |               |              |
| ------------- | ------------- | ------------
| return  | class  | under
| end  | private  | public
| not  | sub  | void
| if  | elsif  | else
| while  | repeat  | for
| from  | by  | read
| or  | and  | print
| int  | flt  | str
| bool  | gt  | lt
| gte  | lte  | eq
| neq  | True | False
| dict  | when |

###Tokens

|               |               |              |
| ------------- | ------------- | ------------
| ID  | CLASS_NAME  | COLON
| MONEY  | PLUS  | MINUS
| MULTIPLY  | DIVIDE  | L_PAREN
| R_PAREN  | COMMA  | L_THAN
| G_THAN  | NOT_EQ  | L_THAN_EQ
| G_THAN_EQ  | EQ_TO  | OR_OP
| AND_OP  | NOT_OP  | CTE_I
| CTE_F  | CTE_STR  | L_SQ_BRACKET
| R_SQ_BRACKET  |   |

###NON TERMINALS

|               |               |              |
| ------------- | ------------- | ------------
| PROGRAM  | BLOCK  | STATEMENT
| RETURN  | CLASS  | EXPRESSION
| MINI_EXPRESSION  | EXP  | TERM
| FACTOR  | CLASS_BLOCK  | FACTOR
| PRIVATE  | PUBLIC  | DECLARATION
| ARR_SIZE  | INITIALIZATION  | ASSIGNMENT
| CONSTRUCTOR  | SUBROUTINE  | RELATIONAL
| LOGICAL  | VAR_CTE_1  | VAR_CTE_2
| VAR_CTE_3  | CTE_B  | WRITE
| CONDITION  | VAR_CTE_1  | CYCLE
| OPERATOR  | ACCESS  | WHEN
| REPEAT  | FOR  | SUB_CALL
| SUB_CALL_ARGS  | ID_CALLS  | TYPE
| READ  |   |

###DATA TYPES

As of this moment, Plz will only have the types Integer, Float, String and Boolean, with the possibility of creating arrays, matrices and dictionaries that contain variables or elements of this types.
The user will also be able to create their own classes and objects.
