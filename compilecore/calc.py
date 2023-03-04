

from .parser import *

class CalcTokenType(TokenType):
    
    PLUS          = '+'
    MINUS         = '-'
    MUL           = '*'
    DIV           = '/'
    LPAREN        = '('
    RPAREN        = ')'
    INTEGER       = 'INTEGER'
    EOF           = 'EOF'


class CalcLexer(Lexer):
    
    def __init__(self, text):
        super().__init__(text)
        
    def peek(self) -> str:
        '''查看下一个字符(不消耗)'''
        peek_pos = self.pos+1
        if peek_pos > len(self.text)-1:
            return None
        else:
            return self.text[peek_pos]

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
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(CalcTokenType.INTEGER, self.integer())

            try:
                # get enum member by value, e.g.
                # TokenType(';') --> TokenType.SEMI
                token = Token(CalcTokenType(self.current_char),self.current_char)
                self.advance()
                return token
            except ValueError:
                # no enum member with value equal to self.current_char
                self.error()

        
        return Token(CalcTokenType.EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class Num(AST):
    ''''''
    def __init__(self, token):
        self.token = token
        self.value = token.value

class CalcParser(Parser):
    
    def __init__(self, lexer):
        super().__init__(lexer)
        self.current_token: Token

    def factor(self):
        """
        factor : INTEGER
               | LPAREN expr RPAREN
        """
        token:Token = self.current_token
        if token.type == CalcTokenType.INTEGER:
            self.eat(CalcTokenType.INTEGER)
            return Num(token)
        elif token.type == CalcTokenType.LPAREN:
            self.eat(CalcTokenType.LPAREN)
            node = self.expr()
            self.eat(CalcTokenType.RPAREN)
            return node
        elif token.type == CalcTokenType.MINUS:
            self.eat(CalcTokenType.MINUS)
            return UnaryOp(op=token, expr=self.factor())
        elif token.type == CalcTokenType.PLUS:
            self.eat(CalcTokenType.PLUS)
            return UnaryOp(op=token, expr=self.factor())
        else:
            self.error(ErrorCode.DUPLICATE_ID, token)

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (CalcTokenType.MUL, CalcTokenType.DIV):
            token:Token = self.current_token
            if token.type == CalcTokenType.MUL:
                self.eat(CalcTokenType.MUL)
            elif token.type == CalcTokenType.DIV:
                self.eat(CalcTokenType.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (CalcTokenType.PLUS, CalcTokenType.MINUS):
            token = self.current_token
            if token.type == CalcTokenType.PLUS:
                self.eat(CalcTokenType.PLUS)
            elif token.type == CalcTokenType.MINUS:
                self.eat(CalcTokenType.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self):
        return self.expr()


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        # type(node).__name__ = BinOp / Num
        method_name = 'visit_' + type(node).__name__
        
        # equal to use : self.visit_BinOp(node) / self.visit_Num(node)
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node:BinOp):
        if node.op.type == CalcTokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == CalcTokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == CalcTokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == CalcTokenType.DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_Num(self, node):
        return node.value
    
    def visit_UnaryOp(self, node):
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
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Exception as e:
            print(e.message)

    