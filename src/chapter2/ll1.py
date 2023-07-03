
from .base import CFGCore
from .utils import print_LL1_table, print_ll1_analysis_table

class LL1(CFGCore):
    
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
        
    def get_analysis_table(self):
        
        # 初始化 LL1 table
        self.LL1_table = {}
        
        non_terminal_symbols = list(self.grammar.non_terminal_symbols)
        non_terminal_symbols.sort()
        
        terminal_symbols = list(self.grammar.terminal_symbols)
        if self.grammar.epsilon in self.grammar.terminal_symbols:
            terminal_symbols.pop(terminal_symbols.index(self.grammar.epsilon))
        terminal_symbols.sort()
        terminal_symbols.append('$')
        for symbol in non_terminal_symbols:
            self.LL1_table[symbol] = {}
            for s in terminal_symbols:
                self.LL1_table[symbol][s] = []
                
        ll1_collision = False
        
        for production, symbols in self.grammar.select_set.items():
            for symbol in symbols:
                production_head = production[0]
                if len(self.LL1_table[production_head][symbol]) != 0:
                    ll1_collision = True
                self.LL1_table[production_head][symbol].append(production)
            
        if ll1_collision:
            word = '不是LL1文法, 存在冲突'
        else:
            word = '是LL1文法'
        print(f'[LL1 TABLE]: {word}')
        print_LL1_table(self.LL1_table, non_terminal_symbols, terminal_symbols)
                
    def LL1_construct(self, string: str):
        
        self.get_analysis_table()
        terminal_symbols = list(self.grammar.terminal_symbols)
        if self.grammar.epsilon in self.grammar.terminal_symbols:
            terminal_symbols.pop(terminal_symbols.index(self.grammar.epsilon))
        terminal_symbols.sort()
        terminal_symbols.append('$')
        
        analysis_record = [['rest string','analysis stack','analysis action']]
        rest_string = string + '$'
        analysis_stack = self.grammar.begin_symbol + '$' # 开始时栈中两个元素
        
        analysis_info = ''
        while analysis_stack:
            
            if len(rest_string) == 0:
                analysis_info = "匹配失败"
                break
            
            stack_symbol = analysis_stack[0]
            rest_string_symbol = rest_string[0]
            
            if stack_symbol in terminal_symbols:
                if stack_symbol == rest_string_symbol:
                    # 相同符号, 消除
                    analysis_record.append([rest_string,analysis_stack,'匹配'])
                    analysis_stack = analysis_stack[1:]
                    rest_string = rest_string[1:]
                else:
                    if rest_string_symbol in terminal_symbols:
                        analysis_info = "匹配失败"
                        break
                    else:
                        analysis_info = f"未知符号: {rest_string_symbol}"
                        break
            else:
                if rest_string_symbol not in terminal_symbols:
                    analysis_info = f"未知符号: {rest_string_symbol}"
                    break
                if len(self.LL1_table[stack_symbol][rest_string_symbol]) > 1:
                    analysis_info = f"{stack_symbol} {rest_string_symbol} 存在LL1冲突, 请手动处理"
                    break
                if len(self.LL1_table[stack_symbol][rest_string_symbol]) == 0:
                    analysis_info = f"{stack_symbol} {rest_string_symbol} 没有匹配项"
                    break
                # 成功分析
                analysis_action = self.LL1_table[stack_symbol][rest_string_symbol][0]
                analysis_record.append([rest_string,analysis_stack,analysis_action]) # 记录
                
                # 'A -> Bxxx'
                production = analysis_action[5:]
                if production == self.grammar.epsilon:
                    production = ''
                analysis_stack = production + analysis_stack[1:]
                
        print_ll1_analysis_table(analysis_record)        
        
        print(analysis_info)
        if len(rest_string) == 0:
            print("LL1分析结束")
        else:
            print("LL1分析失败")