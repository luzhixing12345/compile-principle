
from enum import Enum

class Token(object):
    def __init__(self, type, value, line_number=None, column_number=None):
        self.type = type
        self.value = value
        self.line_number = line_number
        self.column_number = column_number


    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return f"Token({self.type}, {repr(self.value)}, position={self.line_number}:{self.column_number})"

    def __repr__(self):
        return self.__str__()


class CalcTokenType(Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    LPAREN = "("
    RPAREN = ")"
    INTEGER = "INTEGER"
    EOF = "EOF"


class ErrorCode(Enum):
    UNEXPECTED_TOKEN = "Unexpected token"
    ID_NOT_FOUND = "Identifier not found"
    DUPLICATE_ID = "Duplicate id found"
    PARAMETERS_NOT_MATCH = "parameter number not match"
    INVALID_TYPE = "Invalid type"
    TYPE_MISMATCH = "Type mismatch"
    DIVISION_BY_ZERO = "Division by zero"
    UNDEFINED_FUNCTION = "Undefined function"


class Error(Exception):
    def __init__(self, error_code=None, message=None):
        self.error_code = error_code
        self.message = f"{self.__class__.__name__}: {message}"


class LexerError(Error):
    def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)


class ParserError(Error):
    def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)


class InterpreterError(Error):
    def __init__(self, error_code=None, message=None):
        super().__init__(error_code, message)


class SemanticError(Error):
    def __init__(self, error_code=None, token=None, message=None):
        super().__init__(error_code, token, message)


class CalcLexer:
    """词法分析器"""

    def __init__(self, text):
        self.text: str = text
        self.pos = 0
        self.current_char: str = self.text[self.pos]
        self.line_number = 1
        self.column_number = 1

    def error(self) -> Error:
        s = f"Lexer error on '{self.current_char}' (line: {self.line_number} column: {self.column_number})"
        raise LexerError(message=s)

    def advance(self) -> str:
        """读取下一个字符"""
        if self.current_char == "\n":
            self.line_number += 1
            self.column_number = 0

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column_number += 1

    def skip_whitespace(self) -> None:
        """跳过空格"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        """获取整数"""
        result = ""
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
                token = Token(CalcTokenType.INTEGER, self.integer(), self.line_number, self.column_number)
                return token

            try:
                token = Token(CalcTokenType(self.current_char), self.current_char, self.line_number, self.column_number)
                self.advance()
                return token
            except ValueError:
                self.error()

        return Token(CalcTokenType.EOF, None)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class AST(object):
    op: Token


class BinOp(AST):
    """双目运算符"""

    def __init__(self, left, op, right):
        self.left = left
        self.op: Token = op
        self.right = right


class UnaryOp(AST):
    """单目运算符"""

    def __init__(self, op, expr):
        self.op: Token = op
        self.expr = expr


class Num(AST):
    """"""

    def __init__(self, token):
        self.token = token
        self.value = token.value


class CalcParser:
    """语法分析器"""

    def __init__(self, lexer):
        self.lexer: CalcLexer = lexer
        # 初始化时获取第一个token
        self.current_token: Token = self.lexer.get_next_token()
        self.current_token: Token
        self.bracket_number = 0

    def error(self, error_code, token) -> Error:
        raise ParserError(
            error_code=error_code,
            message=f"{error_code.value} -> {token}",
        )

    def eat(self, token_type):
        # 比较当前token类型和传递的token类型
        # 如果它们匹配,则当前令牌 "吃掉"
        # 并将下一个token分配给self.current_token
        # 否则引发一个异常
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

    def factor(self):
        """
        factor : INTEGER
               | LPAREN expr RPAREN
        """
        token: Token = self.current_token
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
            self.error(ErrorCode.UNEXPECTED_TOKEN, token)

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""

        node = self.factor()

        while self.current_token.type in (CalcTokenType.MUL, CalcTokenType.DIV):
            token: Token = self.current_token
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

        if self.current_token.type == CalcTokenType.LPAREN:
            self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)
        if self.current_token.type == CalcTokenType.RPAREN:
            if self.bracket_number <= 0:
                self.error(ErrorCode.UNEXPECTED_TOKEN, self.current_token)

        return node

    def parse(self):
        return self.expr()


###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################


class CalcInterpreter:
    def __init__(self, parser) -> None:
        self.parser: CalcParser = parser

    def visit(self, node):
        # 获取节点类型
        method_name = "visit_" + type(node).__name__
        # 反射
        visit_method = getattr(self, method_name, self.visit_error)
        return visit_method(node)

    def visit_error(self, node) -> Error:
        s = f"找不到 visit_{type(node).__name__} 方法, 需要编写 {type(node).__name__} 类的对应visit方法"
        raise InterpreterError(s, type(node).__name__)

    def error(self, error_code: ErrorCode, node) -> Error:
        raise InterpreterError(
            error_code=error_code,
            message=f"{error_code.value} -> {node}",
        )

    def visit_BinOp(self, node: BinOp):
        if node.op.type == CalcTokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == CalcTokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == CalcTokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == CalcTokenType.DIV:
            divsor = self.visit(node.right)
            if divsor == 0:
                self.error(ErrorCode.DIVISION_BY_ZERO, divsor)
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


def main():
    while True:
        text = input("calc> ")
        try:
            lexer = CalcLexer(text)
            parser = CalcParser(lexer)
            interpreter = CalcInterpreter(parser)
            result = interpreter.interpret()
            print(result)
        except Error as e:
            print(e.message)


if __name__ == "__main__":
    main()
