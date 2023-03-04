
from enum import Enum

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND     = 'Identifier not found'
    DUPLICATE_ID     = 'Duplicate id found'
    PARAMETERS_NOT_MATCH = 'parameter number not match'


class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        self.message = f'{self.__class__.__name__}: {message}'

class LexerError(Error):
    
    def __init__(self, error_code=None, token=None, message=None):
        super().__init__(error_code, token, message)

class ParserError(Error):
    
    def __init__(self, error_code=None, token=None, message=None):
        super().__init__(error_code, token, message)

class SemanticError(Error):
    
    def __init__(self, error_code=None, token=None, message=None):
        super().__init__(error_code, token, message)
