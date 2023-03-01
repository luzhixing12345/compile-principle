
import os
import logging
import itertools


class Core:

    def __init__(self, file_path='') -> None:
        '''上下文无关文法 Context-Free Grammar(CFG)'''
        
        self.file_content = None
        self.grammar = Grammar()
        self.logger = Logger()
        self.parse_file(file_path)

    def parse_file(self, file_path: str):

        if file_path == '':
            return

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            self.file_content = f.read().split('\n')

    def parse_grammar(self):
        '''解析产生式'''
        if self.file_content is None:
            self.log("类初始化请传入 'file_path' 或无参数初始化之后调用 'parse_file' 读取文件")
            return
        if len(self.file_content) == 0:
            self.log('文件内容为空')
            exit()
        # 文法展开
        for i in range(len(self.file_content)):
            line = self.file_content[i]
            production_rule = line.split('->')
            if len(production_rule) != 2:
                self.log(line, "不符合产生式规范: S -> A | b")
                exit()
            production_head = production_rule[0].strip()
            if len(production_head) != 1:
                self.log("产生式规则的左侧应为单个终结符: " + production_head)
                exit()

            if i == 0:
                self.grammar.begin_symbol = production_head  # 起始符号

            if self.grammar.productions.get(production_head) is None:
                self.grammar.productions[production_head] = []
            # 展开所有产生式
            production_bodys = production_rule[1].split('|')
            for production_body in production_bodys:
                production_body = production_body.strip()
                if self.grammar.epsilon in production_body and len(production_body) != 1:
                    self.log(f"产生式 {production_body} 中不应出现 {self.grammar.epsilon}")
                    exit()
                self.grammar.productions[production_head].append(production_body)

        self.grammar.parse()
        self.log(self.grammar, debug=True)

    def debug(self):
        '''设置日志等级为DEBUG: 展示更多信息'''
        self.logger.set_level(logging.DEBUG)

    def log(self, info: str, debug=False):
        return self.logger.log(info, debug)

    def print_table(self, name ,table, debug = False):
        self._split_line(name, debug = debug)

        max_str_length = max(len(s) for s in table.keys()) + 1
        for key, value in table.items():
            self.log(f'   {key:<{max_str_length}}: {str(value)}', debug = debug)
        self._split_line(debug = debug)

    def _split_line(self, name="", debug = False):

        if name != "":
            self.log('*' + name + '*\n', debug = debug)
        else:
            self.log('', debug = debug)

class Logger:

    def __init__(self) -> None:

        # 创建一个名为 "my_logger" 的 Logger 对象
        self.logger = logging.getLogger('CompileCore Logger')
        self.logger.setLevel(logging.INFO)

        # 创建一个将日志记录到终端的 StreamHandler 对象
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # 添加处理器到 Logger 对象
        self.logger.addHandler(console_handler)

    def set_level(self, log_level):
        '''设置日志级别'''
        self.logger.setLevel(log_level)

    def log(self, info, debug=False):
        if debug:
            self.logger.debug(info)
        else:
            self.logger.info(info)


class Grammar:

    def __init__(self) -> None:

        self.begin_symbol = 'S'
        self.epsilon = 'ε'
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.productions = {}

    def __str__(self) -> str:

        output_str = f'起始符号: {self.begin_symbol}\n'
        output_str += '产生式:\n'
        for production_head, production_bodys in self.productions.items():
            for production_body in production_bodys:
                output_str += f'  {production_head} -> {production_body}\n'
        output_str += f'非终结符: {str(self.non_terminal_symbols)}\n'
        output_str += f'终结符: {str(self.terminal_symbols)}\n'
        return output_str

    def parse(self):
        # 产生式左侧的是非终结符
        self.non_terminal_symbols = list(self.productions.keys())
        # 在右侧但不在左侧的符号是终结符
        for production_body in itertools.chain.from_iterable(self.productions.values()):
            for symbol in production_body:
                if symbol not in self.non_terminal_symbols:
                    self.terminal_symbols.append(symbol)
