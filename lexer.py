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
  'sub' : "SUB",
  'void' : "VOID",
  'if' : "IF",
  'elsif' : "ELSIF",
  'else' : "ELSE",
  'while' : "WHILE",
  'repeat' : "REPEAT",
  'for' : "FOR",
  'from' : "FROM",
  'by' : 'BY',
  'read' : 'READ',
  'or' : 'OR',
  'and' : 'AND',
  'not' : 'NOT',
  'print' : 'PRINT',
  'int' : 'INT',
  'flt' : 'FLT',
  'bool' : 'BOOL',
  'gt' : 'GT',
  'lt' : 'LT',
  'gte' : 'GTE',
  'lte' : 'LTE',
  'eq' : 'EQ',
  'neq' : 'NEQ',
}

tokens = [

] + list(reserved.values())
