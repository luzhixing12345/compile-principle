
from enum import Enum

class ErrorCode(Enum):
    
    @classmethod
    def info(cls):
        '''显示所有token类型'''
        max_length = 0
        for member in cls:
            max_length = max(max_length, len(member.name))
        for member in cls:
            print(f'{member.name:<{max_length}}  {member.value}')

class Error(Exception):
    def __init__(self, error_code=None, message=None):
        self.error_code = error_code
        self.message = f'{self.__class__.__name__}: {message}'

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
