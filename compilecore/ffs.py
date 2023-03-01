import copy
from .base import Core

class FFS(Core):
    
    def __init__(self, file_path='') -> None:
        super().__init__(file_path)
        self.first_set = None
        self.follow_set = None
        self.select_set = None
    
    def calculate_first_set(self):
        self.parse_grammar()
        
        init_first_set = {}
        for non_terminal_symbol in self.grammar.non_terminal_symbols:
            # 使用set去重
            init_first_set[non_terminal_symbol] = set()
        
        self.first_set = self._calculate_first_set(init_first_set)
        self._print_set("最终first set",self.first_set)
        
    def _calculate_first_set(self, first_set):
        
        current_frist_set = copy.deepcopy(first_set)
        
        for production_head, production_bodys in self.grammar.productions.items():
            for production_body in production_bodys:
                for i in range(len(production_body)):
                    char = production_body[i]
                    if char in self.grammar.terminal_symbols:
                        # 如果char字符是一个终结符
                        # 将char加入到production_statement的first集,结束
                        first_set[production_head].add(char)
                        break
                    else:
                        # char字符是非终结符
                        # 将char的first集(除去ε) 加入到production_statement的first集中
                        
                        exist_empty = False # char的first集中是否包含ε
                        for c in first_set[char]:
                            if c != self.grammar.epsilon:
                                first_set[production_head].add(c)
                            else:
                                exist_empty = True
                        
                        if not exist_empty:
                            # 如果char的first集中不包含'ε', 则结束
                            break
                        else:
                            # 如果包含了ε, 那么继续判断下一个字符
                            # 如果该字符已经是产生式的最后一个字符,则将ε加入到first集中
                            if i == len(production_body) - 1:
                                first_set[production_head].add(self.grammar.epsilon)
        
        if current_frist_set == first_set:
            # over
            return first_set
        else:
            # self._print_set("当前first set",first_set)
            return self._calculate_first_set(first_set)

    def calculate_follow_set(self):
        
        if self.first_set is None:
            self.calculate_first_set()
            
        init_follow_set = {}
        for non_terminal_symbol in self.grammar.non_terminal_symbols:
            init_follow_set[non_terminal_symbol] = set()
        # 将 $ 加入到起始元素的follow集中
        init_follow_set[self.grammar.begin_symbol].add('$')
        
        self.follow_set = self._calculate_follow_set(init_follow_set)
        self._print_set("最终follow set", self.follow_set)
    
    def _calculate_follow_set(self, follow_set):
        
        current_follow_set = copy.deepcopy(follow_set)
        
        for production_head, production_bodys in self.grammar.productions.items():
            for production_body in production_bodys:
                for i in range(len(production_body)):
                    char = production_body[i]
                    
                    # 如果是终结符则看下一个
                    # 如果是非终结符
                    if char in self.grammar.non_terminal_symbols:
                        for j in range(i+1, len(production_body)):
                            # 找到后面的符号
                            follow_char = production_body[j]
                            if follow_char in self.grammar.terminal_symbols:
                                # 如果是终结符, 则加入到char的follow集中,结束
                                follow_set[char].add(follow_char)
                                break
                            else:
                                # 如果是非终结符,则将follow_char的first集的元素加入到
                                # char的follow集中
                                for symbol in self.first_set[follow_char]:
                                    follow_set[char].add(symbol)
                                # 如果char的follow集中有 ε 则去掉 ε 继续
                                if self.grammar.epsilon in follow_set[char]:
                                    follow_set[char].remove(self.grammar.epsilon)
                                else:
                                    # 如果没有 ε 则结束
                                    break
                for i in range(len(production_body)-1,-1,-1):
                    char = production_body[i]
                    # 如果结尾是一个终结符,则结束
                    # 如果结尾元素是一个非终结符
                    # 那么将产生式头部的follow集加入到结尾元素的follow集中
                    if char in self.grammar.terminal_symbols:
                        break
                    else:
                        for symbol in follow_set[production_head]:
                            follow_set[char].add(symbol)
                        # 如果结尾元素的follow集中不含 ε 则结束
                        # 否则继续向前判断
                        if self.grammar.epsilon not in self.first_set[char]:
                            break
        if current_follow_set == follow_set:
            # over
            return follow_set
        else:
            # self._print_set("当前follow集", follow_set)
            return self._calculate_follow_set(follow_set)
        
    def calculate_select_set(self):
        
        if self.first_set is None:
            self.calculate_first_set()
        if self.follow_set is None:
            self.calculate_follow_set()
    
        self.select_set = {}
        
        for production_head, production_bodys in self.grammar.productions.items():
            for production_body in production_bodys:
                first_char = production_body[0]
                
                production = f'{production_head} -> {production_body}'
                if first_char == self.grammar.epsilon:
                    # 如果产生式的第一个字符为 ε
                    # 该产生式的select集是production_head的follow集
                    self.select_set[production] = self.follow_set[production_head]
                elif first_char in self.grammar.terminal_symbols:
                    # 如果第一个字符是终结符
                    # 该产生式的select集是这个字符
                    self.select_set[production] = set(first_char)
                else:
                    # 如果第一个字符是非终结符
                    # 该产生式的select集是第一个字符的first集
                    self.select_set[production] = self.first_set[first_char]
        
        self._print_set('select集',self.select_set)
        return self.select_set
    
    def run(self):
        
        return self.calculate_select_set()