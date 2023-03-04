

from .token import Token

class AST(object):
    op: Token

class BinOp(AST):
    '''双目运算符'''
    def __init__(self, left, op, right):
        self.left = left
        self.op:Token = op
        self.right = right

class UnaryOp(AST):
    '''单目运算符'''
    def __init__(self, op, expr):
        self.op:Token = op
        self.expr = expr

