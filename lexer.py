# Erik Torres A01196362
# Diego Astiazaran A01243969
import ply.lex as lex

reserved = {
   'return' : "RETURN",
   'class' : "CLASS",
   'under' : "UNDER",
   'end' : "END",
   'private' : "PRIVATE",
   'public' : "PUBLIC",
   'not' : "NOT",
   'sub' : "SUB",
   'void' : "VOID",
   'if' : "IF",
   'elsif' : "ELSIF",
   'else' : "ELSE",
   'while' : "WHILE",
   'repeat' : "REPEAT",
   'for' : "FOR",
   'from' : "FROM",
}

tokens = [

] + list(reserved.values())
