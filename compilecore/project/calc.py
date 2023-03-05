

from ..parser import *
import inspect

calc_logger = Logger()
# calc_logger.debug()

class CalcTokenType(TokenType):
    
    PLUS          = '+'
    MINUS         = '-'
    MUL           = '*'
    DIV           = '/'
    LPAREN        = '('
    RPAREN        = ')'
    INTEGER       = 'INTEGER'
    EOF           = 'EOF'

class CalcError(ErrorCode):
    
    UNEXPECTED_TOKEN     = 'Unexpected token'
    ID_NOT_FOUND         = 'Identifier not found'
    DUPLICATE_ID         = 'Duplicate id found'
    PARAMETERS_NOT_MATCH = 'parameter number not match'
    INVALID_TYPE         = 'Invalid type'
    TYPE_MISMATCH        = 'Type mismatch'
    DIVISION_BY_ZERO     = 'Division by zero'
    UNDEFINED_FUNCTION   = 'Undefined function'

class CalcLexer(Lexer):
    '''词法分析器'''
    
    def __init__(self, text):
        super().__init__(text)

    def skip_whitespace(self) -> None:
        '''跳过空格'''
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        '''获取整数'''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                token = Token(CalcTokenType.INTEGER, self.integer(),self.line_number, self.column_number)
                calc_logger.log(token)
                return token

            try:
                token = Token(CalcTokenType(self.current_char),self.current_char, self.line_number, self.column_number)
                self.advance()
                calc_logger.log(token)
                return token
            except ValueError:
                self.error()

        calc_logger.log('end')
        return Token(CalcTokenType.EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


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

class Num(AST):
    ''''''
    def __init__(self, token):
        self.token = token
        self.value = token.value

class CalcParser(Parser):
    '''语法分析器'''
    
    def __init__(self, lexer):
        super().__init__(lexer)
        self.current_token: Token
        self.bracket_number = 0

    def factor(self):
        """
        factor : INTEGER
               | LPAREN expr RPAREN
        """
        calc_logger.log(f'called {inspect.currentframe().f_code.co_name}')
        token:Token = self.current_token
        if token.type == CalcTokenType.INTEGER:
            self.eat(CalcTokenType.INTEGER)
            return Num(token)
        elif token.type == CalcTokenType.LPAREN:
            self.eat(CalcTokenType.LPAREN)
            self.bracket_number += 1
            node = self.expr()
            self.eat(CalcTokenType.RPAREN)
            self.bracket_number -= 1
            return node
        elif token.type == CalcTokenType.MINUS:
            self.eat(CalcTokenType.MINUS)
            return UnaryOp(op=token, expr=self.factor())
        elif token.type == CalcTokenType.PLUS:
            self.eat(CalcTokenType.PLUS)
            return UnaryOp(op=token, expr=self.factor())
        else:
            self.error(CalcError.UNEXPECTED_TOKEN, token)

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        calc_logger.log(f'called {inspect.currentframe().f_code.co_name}')
        node = self.factor()

        while self.current_token.type in (CalcTokenType.MUL, CalcTokenType.DIV):
            token:Token = self.current_token
            if token.type == CalcTokenType.MUL:
                calc_logger.log("eat mul in term")
                self.eat(CalcTokenType.MUL)
            elif token.type == CalcTokenType.DIV:
                calc_logger.log("eat div in term")
                self.eat(CalcTokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        calc_logger.log(f'called {inspect.currentframe().f_code.co_name}')
        node = self.term()

        while self.current_token.type in (CalcTokenType.PLUS, CalcTokenType.MINUS):
            token = self.current_token
            if token.type == CalcTokenType.PLUS:
                calc_logger.log("eat plus in expr")
                self.eat(CalcTokenType.PLUS)
            elif token.type == CalcTokenType.MINUS:
                calc_logger.log("eat minus in expr")
                self.eat(CalcTokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())
        
        if self.current_token.type == CalcTokenType.LPAREN:
            self.error(CalcError.UNEXPECTED_TOKEN, self.current_token)
        if self.current_token.type == CalcTokenType.RPAREN:
            if self.bracket_number <= 0:
                self.error(CalcError.UNEXPECTED_TOKEN,self.current_token)
            
        return node

    def parse(self):
        return self.expr()


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class CalcInterpreter(ASTVisitor):
    
    def __init__(self, parser) -> None:
        super().__init__(parser)
    
    def visit_BinOp(self, node:BinOp):
        if node.op.type == CalcTokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == CalcTokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == CalcTokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == CalcTokenType.DIV:
            divsor = self.visit(node.right)
            if divsor == 0:
                self.error(CalcError.DIVISION_BY_ZERO,divsor)
            return self.visit(node.left) // divsor

    def visit_Num(self, node: Num):
        return node.value
    
    def visit_UnaryOp(self, node: UnaryOp):
        op = node.op.type
        if op == CalcTokenType.PLUS:
            return +self.visit(node.expr)
        elif op == CalcTokenType.MINUS:
            return -self.visit(node.expr)

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def calculator():
    
    while True:
        text = input('calc> ')
        try:
            lexer = CalcLexer(text)
            parser = CalcParser(lexer)
            interpreter = CalcInterpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e.message)

    