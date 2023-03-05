

from .error import LexerError, Error
from .token import Token

class Lexer(object):
    def __init__(self, text):
        self.text:str = text
        self.pos = 0
        self.current_char:str = self.text[self.pos]
        self.line_number = 1
        self.column_number = 1

    def error(self) -> Error:
        s = f"Lexer error on '{self.current_char}' (line: {self.line_number} column: {self.column_number})"
        raise LexerError(message=s)

    def advance(self) -> str:
        '''读取下一个字符'''
        if self.current_char == '\n':
            self.line_number += 1
            self.column_number = 0
        
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            self.column_number += 1

    def get_next_token(self) -> Token:
        """获取下一个token"""
        raise NotImplementedError
