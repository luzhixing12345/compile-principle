import copy
from .base import Core

class FFS(Core):
    
    def __init__(self, file_path='') -> None:
        super().__init__(file_path)
        
    
    def calculate_first_set(self):
        self.parse_grammar()
        self.first_set = {}
        for non_terminal_symbol in self.grammar.non_terminal_symbols:
            self.first_set[non_terminal_symbol] = set()
        self._calculate_first_set(self.first_set)
        
    def _calculate_first_set(self, first_set = {}):
        
        self.first_set = first_set
        current_frist_set = copy.deepcopy(self.first_set)
        
        for production_statement, production_alternatives in self.grammar.productions.items():
            for production_alternative in production_alternatives:
                for i in range(len(production_alternative)):
                    char = production_alternative[i]
                    if char in self.grammar.terminal_symbols:
                        # 如果char字符是一个终结符
                        # 将char加入到production_statement的first集,结束
                        self.first_set[production_statement].add(char)
                        break
                    else:
                        # char字符是非终结符
                        # 将char的first集(除去ε) 加入到production_statement的first集中
                        
                        exist_empty = False # char的first集中是否包含ε
                        for c in self.first_set[char]:
                            if c != self.epsilon:
                                self.first_set[production_statement].add(c)
                            else:
                                exist_empty = True
                        
                        if not exist_empty:
                            # 如果char的first集中不包含'ε', 则结束
                            break
                        else:
                            # 如果包含了ε, 那么继续判断下一个字符
                            # 如果该字符已经是产生式的最后一个字符,则将ε加入到first集中
                            if i == len(production_alternative) - 1:
                                self.first_set[production_statement].add(self.epsilon)
        
        if current_frist_set == self.first_set:
            # over
            self.print_table("最终first set",self.first_set)
            return
        else:
            self.print_table("当前first set", self.first_set, debug=True)
            return self._calculate_first_set(self.first_set)

    def calculate_follow_set(self):
        ...
        
    def calculate_select_set(self):
        
        ...
        
    