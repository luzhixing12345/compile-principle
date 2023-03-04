
# RE - NFA - DFA
# https://www.geeksforgeeks.org/converting-epsilon-nfa-to-dfa-using-python-and-graphviz/

from .parser import *

class RETokenType(TokenType):
    
    ASTERISK       = '*' # 0次或多次
    ALTERNATION    = '|' # 或
    LEFT_GROUP     = '(' # 分组
    RIGHT_GROUP    = ')' #
    PLUS           = '+' # 1次或多次
    QMARK          = '?' # 0/1
    DOT            = '.' # 任意字符
    CONCAT         = ''  # 空格/不加公开
    # CARET          = '^' # 字符串开始
    # DOLLAR_SIGN    = '$' # 字符串结束
    # LEFT_BRACKETS  = '[' # 
    # RIGHT_BRACKETS = ']'
    CHAR           = 'CHAR' # 原子符号
    EOF            = 'EOF'

class RELexer(Lexer):
    
    def __init__(self, text):
        super().__init__(text)

    def get_next_token(self):
        while self.current_char is not None:

            # 处理转义字符
            # 把下一个字符当作CHARACTER处理
            if self.current_char == '\\':
                self.advance()
                token = Token(RETokenType.CHAR,self.current_char)
                self.advance()
                return token

            token = Token(RETokenType(self.current_char),self.current_char)
        
        return Token(RETokenType.EOF, None)


class CHAR_AST(AST):
    
    def __init__(self, token) -> None:
        self.token = token

class REParser(Parser):
    
    def __init__(self, lexer):
        super().__init__(lexer)
    
    def atom(self):
        '''
        atom   : CHAR
               | DOT
               | LPAREN regex RPAREN
        '''
        token:Token = self.current_token
        if token.type == RETokenType.CHAR:
            self.eat(RETokenType.CHAR)
            return CHAR_AST(token)
        elif token.type == RETokenType.LEFT_GROUP:
            self.eat(RETokenType.LEFT_GROUP)
            node = self.regex()
            self.eat(RETokenType.RIGHT_GROUP)
            return node
        else:
            self.error(ErrorCode.UNEXPECTED_TOKEN,token)
    
    def factor(self):
        '''
        factor : atom ((STAR | PLUS | QMARK) atom)*
        '''
        node = self.atom()
        
        while self.current_token.type in (RETokenType.ASTERISK, RETokenType.PLUS, RETokenType.QMARK):
            token:Token = self.current_token
            if token.type == RETokenType.ASTERISK:
                self.eat()
    
    def term(self):
        '''
        term   : factor ((CONCAT) factor)*
        '''
        
        
    
    def regex(self):
        '''
        regex  : term ((OR) term)* | EPSILON
        term   : factor ((CONCAT) factor)*
        factor : atom ((STAR | PLUS | QMARK) atom)*
        atom   : CHAR | DOT | LPAREN regex RPAREN
        '''
        node = self.term()
        
    
    def parse(self):
        return self.regex()

class RE:
    
    def __init__(self, pattern) -> None:
        
        self.pattern = pattern
        
        
class NFA:
    
    def __init__(self, lexer) -> None:
        self.lexer:RELexer = lexer



class DFA:
    
    def __init__(self, nfa: NFA) -> None:
        
        self.nfa:NFA = nfa
    
    def match(self, string):
        
        print(True)
    
def regexp(pattern: str, string: str):
    
    lexer = RELexer(pattern)
    nfa = NFA(lexer)
    dfa = DFA(nfa)
    
    return dfa.match(string)