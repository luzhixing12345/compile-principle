
from .base import Core

class LL1(Core):
    
    def __init__(self, file_path) -> None:
        super().__init__(file_path)
        
    def get_analysis_table(self):
        
        LL1_table = []
        select_set = self.ffs.calculate_select_set()
        terminal_symbols = list(self.ffs.grammar.terminal_symbols)
        terminal_symbols.sort()
        if self.ffs.grammar.epsilon in self.ffs.grammar.terminal_symbols:
            terminal_symbols.pop(terminal_symbols.index(self.ffs.grammar.epsilon))
        terminal_symbols.append('$')
        terminal_symbols.insert(0, ' ')
        LL1_table.append(terminal_symbols) # 表格头
        non_terminal_symbols = list(self.ffs.grammar.non_terminal_symbols)
        non_terminal_symbols.sort()
        for symbol in non_terminal_symbols:
            line = [symbol] + ['|'] * (len(terminal_symbols) - 1)
            LL1_table.append(line)
        
        ll1_collision = False
        
        for production, symbols in select_set.items():
                        
            row = non_terminal_symbols.index(production[0]) + 1
            for symbol in symbols:
                col = terminal_symbols.index(symbol)
                if LL1_table[row][col] != '|':
                    ll1_collision = True
                LL1_table[row][col] += ' ' + production
        
        if ll1_collision:
            word = '不是LL1文法, 存在冲突'
        else:
            word = '是LL1文法'
        print(f'[LL1 TABLE]: {word}')
        self._print_table(LL1_table)

    def _print_table(self, table):
        max_lengths = [max([len(str(row[i])) for row in table]) for i in range(len(table[0]))]

        # 打印表头
        for i, header in enumerate(table[0]):
            print(f"{header:<{max_lengths[i]}}", end=' ')
        print()
        # 打印分隔符
        for length in max_lengths:
            print("-" * length, end=' ')
        print()
        # 打印数据行
        for row in table[1:]:
            for i, item in enumerate(row):
                print(f"{item:<{max_lengths[i]}}", end=' ')
            print()
                
    def LL1_construct(self):
        
        ...            
    
    def run(self):
        self.get_analysis_table()