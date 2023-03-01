
import os
import logging
import itertools
import re

class Core:

    def __init__(self, file_path='') -> None:
        '''上下文无关文法 Context-Free Grammar(CFG)'''
        
        self.file_content:str = None
        self.grammar:Grammar = Grammar()
        self.parse_file(file_path)

    def parse_file(self, file_path: str):

        if file_path == '':
            return

        exam_path = re.findall(re.compile(r'e:(\d+):(\d+)'),file_path)
        
        if len(exam_path) == 1 and len(exam_path[0]) == 2:
            file_path = os.path.join(os.path.dirname(__file__),'exam',exam_path[0][0],exam_path[0][1] + '.txt')

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            self.file_content = f.read().split('\n')

    def parse_grammar(self):
        '''解析产生式'''

        if self.file_content is None:
            print("类初始化请传入 'file_path' 或无参数初始化之后调用 'parse_file' 读取文件")
            return
        if len(self.file_content) == 0:
            print('文件内容为空')
            exit()
        # 文法展开
        for i in range(len(self.file_content)):
            line = self.file_content[i]
            production_rule = line.split('->')
            if len(production_rule) != 2:
                print(line, "不符合产生式规范: S -> A | b")
                exit()
            production_head = production_rule[0].strip()
            if len(production_head) != 1:
                print("产生式规则的左侧应为单个终结符: " + production_head)
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
                    print(f"产生式 {production_body} 中不应出现 {self.grammar.epsilon}")
                    exit()
                self.grammar.productions[production_head].append(production_body)

        self.grammar.parse()
        print(self.grammar)

    def run(self):
        
        raise NotImplementedError

    def _print_set(self, name ,table):
        self._split_line(name)

        max_str_length = max(len(s) for s in table.keys()) + 1
        for key, value in table.items():
            print(f'   {key:<{max_str_length}}: {str(value)}')
        self._split_line()

    def _split_line(self, name=""):

        if name != "":
            print('*' + name + '*\n')
        else:
            print('')

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
        self.non_terminal_symbols = list(set(self.productions.keys()))
        self.non_terminal_symbols.sort()
        # 在右侧但不在左侧的符号是终结符
        for production_body in itertools.chain.from_iterable(self.productions.values()):
            for symbol in production_body:
                if symbol not in self.non_terminal_symbols:
                    self.terminal_symbols.append(symbol)
        self.terminal_symbols = list(set(self.terminal_symbols))
        self.terminal_symbols.sort()