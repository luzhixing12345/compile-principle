
import os
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
        print(name)
        max_str_length = max(len(s) for s in table.keys()) + 1
        for key, value in table.items():
            print(f'   {key:<{max_str_length}}: {str(value)}')
        print()

class Grammar:

    def __init__(self) -> None:

        self.begin_symbol = 'S'
        self.epsilon = 'ε'
        self.non_terminal_symbols = set()
        self.terminal_symbols = set()
        self.productions = {}

    def __str__(self) -> str:

        
        output_str = f'[起始符号]: {self.begin_symbol}\n'
        output_str += '[产生式]:\n'
        for production_head, production_bodys in self.productions.items():
            for production_body in production_bodys:
                output_str += f'  {production_head} -> {production_body}\n'
        output_str += f'[非终结符]: {str(self.non_terminal_symbols)}\n'
        output_str += f'[终结符  ]: {str(self.terminal_symbols)}\n'
        return output_str
    

    def parse(self):
        # 产生式左侧的是非终结符
        self.non_terminal_symbols = set(self.productions.keys())
        # 在右侧但不在左侧的符号是终结符
        for production_body in itertools.chain.from_iterable(self.productions.values()):
            for symbol in production_body:
                if symbol not in self.non_terminal_symbols:
                    self.terminal_symbols.add(symbol)
        self.terminal_symbols = set(self.terminal_symbols)
        
        self.eliminate_left_recursion()
        
    def eliminate_left_recursion(self):
        self.eliminate_indirect_left_recursion()
        self.eliminate_direct_left_recursion()        
        
    def eliminate_indirect_left_recursion(self):
        ...
        
        
    def eliminate_direct_left_recursion(self):
        
        flag = False
        extend_productions = {}
        
        for production_head, production_bodys in self.productions.items():
            for production_body in production_bodys:
                if production_body[0] == production_head:
                    flag = True
                    break
            if flag:
                # 存在直接左递归
                print(f"[{production_head} 存在直接左递归]")
                new_symbol = self._register_new_symbol()
                # P -> Pα1 | Pα2 | Pαn | β1 | β2 | βm
                #
                # P -> β1P' | β2P' | βmP'     (1)
                # P'-> α1P' | α2P' | αnP' | ε (2)
                
                new_productions = [self.epsilon] # 新符号的产生式集合
                head_productions = [] # 存在左递归的head的新产生式集合
                for production_body in production_bodys:
                    if production_body[0] == production_head:
                        # 情况(2)
                        new_productions.append(production_body[1:] + new_symbol)
                    else:
                        # 情况(1)
                        if production_body == self.epsilon:
                            production_body = ''
                        head_productions.append(production_body + new_symbol)
                
                extend_productions[new_symbol] = new_productions
                self.productions[production_head] = head_productions
                flag = False
        # 遍历结束统一添加
        for new_symbol, new_productions in extend_productions.items():
            self.productions[new_symbol] = new_productions
        
    def _register_new_symbol(self):
        '''选择一个新的非终结符修正原文法'''
        for i in range(ord('A'), ord('Z') + 1):
            new_symbol = chr(i)
            if new_symbol not in self.non_terminal_symbols and \
                new_symbol not in self.terminal_symbols:

                self.non_terminal_symbols.add(new_symbol)
                self.terminal_symbols.add(self.epsilon)
                return new_symbol
        
        for i in range(ord('a'), ord('z') + 1):
            new_symbol = chr(i) 
            if new_symbol not in self.non_terminal_symbols and \
                new_symbol not in self.terminal_symbols:

                self.non_terminal_symbols.add(new_symbol)
                self.terminal_symbols.add(self.epsilon)
                return new_symbol
        
        raise ValueError("没有可用字符")
    