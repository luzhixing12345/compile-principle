
import os
import logging

class Core:
    
    def __init__(self, file_path='') -> None:
        '''上下文无关文法 Context-Free Grammar(CFG)'''
        self.epsilon = 'ε'
        self.file_content = None
        self.grammar = None
        self.logger = Logger()
        self.parse_file(file_path)
        self.parse_grammar()
        
    def parse_file(self, file_path: str):
        
        if file_path == '':
            return
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)
    
        with open(file_path,'r',encoding='utf-8') as f:
            self.file_content = f.read().split('\n')
    
    def parse_grammar(self):
        
        if self.file_content is None:
            self.log("类初始化请传入 'file_path' 或无参数初始化之后调用 'parse_file' 读取文件")
            return
        # 文法展开
        self.grammar = []
        for line in self.file_content:
            production_rule = line.split('->')
            if len(production_rule) != 2:
                self.log(line, '不符合产生式规范: S -> A | b')
                exit()
            production_statement = production_rule[0].strip()
            if len(production_statement) != 1:
                self.log("产生式规则的左侧应为单个终结符:",production_statement)
                exit()
    
    def set_level(self, log_level):
        
        self.logger.set_level(log_level)
                
    def log(self, info:str):
        return self.logger.log(info)
            
class Logger:
    
    def __init__(self) -> None:
        
        # 创建一个名为 "my_logger" 的 Logger 对象
        self.logger = logging.getLogger('CompileCore Logger')
        self.logger.setLevel(logging.DEBUG)

        # 创建一个将日志记录到终端的 StreamHandler 对象
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 添加处理器到 Logger 对象
        self.logger.addHandler(console_handler)
    
    def set_level(self, log_level):
        '''设置日志级别'''
        print('?')
        self.logger.setLevel(log_level)
    
    def log(self, info):
        
        self.logger.debug(info)
    