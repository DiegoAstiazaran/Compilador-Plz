from constants import Operators, QuadOperations
import operator

operations = {
  Operators.PLUS : operator.add,
  Operators.MINUS : operator.sub,
  Operators.MULTIPLY : operator.mul,
  Operators.DIVIDE : operator.truediv,
  Operators.L_THAN : operator.lt,
  Operators.LT : operator.lt,
  Operators.G_THAN : operator.gt,
  Operators.GT : operator.gt,
  Operators.L_THAN_EQ : operator.le,
  Operators.LTE : operator.le,
  Operators.G_THAN_EQ : operator.ge,
  Operators.GTE : operator.ge,
  Operators.NOT_EQ : operator.ne,
  Operators.NEQ : operator.ne,
  Operators.EQ_TO : operator.eq,
  Operators.EQ : operator.eq,
  Operators.AND_OP : operator.and_,
  Operators.AND : operator.and_,
  Operators.OR_OP : operator.or_,
  Operators.OR : operator.or_,
  Operators.NOT_OP : operator.not_,
  Operators.NOT : operator.not_,
  QuadOperations.PLUS_UNARY : operator.pos,
  QuadOperations.MINUS_UNARY : operator.neg,
}