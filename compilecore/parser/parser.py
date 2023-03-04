

from .token import Token
from .lexer import Lexer
from .error import ParserError


class Parser(object):
    def __init__(self, lexer):
        self.lexer:Lexer = lexer
        # 初始化时获取第一个token
        self.current_token:Token = self.lexer.get_next_token()

    def error(self, error_code, token):
        raise ParserError(
            error_code=error_code,
            token=token,
            message=f'{error_code.value} -> {token}',
        )

    def eat(self, token_type):
        # 比较当前token类型和传递的token类型
        # 如果它们匹配，则当前令牌 "吃掉"
        # 并将下一个token分配给self.current_token
        # 否则引发一个异常
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
