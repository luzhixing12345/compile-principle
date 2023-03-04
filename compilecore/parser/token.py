
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
        return f'Token({self.type}, {repr(self.value)}, position={self.line_number}:{self.column_number})'

    def __repr__(self):
        return self.__str__()
    

class TokenType(Enum):
    '''token的枚举类型'''
    
    @classmethod
    def info(cls):
        '''显示所有token类型'''
        max_length = 0
        for member in cls:
            max_length = max(max_length, len(member.name))
        for member in cls:
            print(f'{member.name:<{max_length}}  {member.value}')


# def build_token_types()