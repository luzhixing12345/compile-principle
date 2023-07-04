



def print_set(name ,table):
    print(name)
    max_str_length = max(len(s) for s in table.keys()) + 1
    for key, value in table.items():
        print(f'   {key:<{max_str_length}}: {str(value)}')
    print()
    
def print_LL1_table(table, non_terminal_symbols, terminal_symbols):
    print()
    max_lengths = {}
    for ts in terminal_symbols:
        max_length = 0
        for nts in non_terminal_symbols:
            string_length = 0
            for production in table[nts][ts]:
                string_length += len(production) + 3
            max_length = max(max_length, string_length)
        max_lengths[ts] = max_length

    # 打印表头
    print('  ',end='')
    for ts in terminal_symbols:
        print(f"{ts:^{max_lengths[ts]}}", end=' ')
    print()
    # 打印分隔符
    print('--',end='')
    for ts in terminal_symbols:
        print("-" * max_lengths[ts], end=' ')
    print()
    # 打印数据行
    for nts in non_terminal_symbols:
        print(nts + '|', end='')
        for ts in terminal_symbols:
            string = ''
            for production in table[nts][ts]:
                string += '  ' + production
            print(f"{string:<{max_lengths[ts]}}", end=' ')
        print()
        
def print_ll1_analysis_table(record):
    
    max_lengths = [0,0,0]
    print()
    for i in range(len(record)):
        for j in range(3):
            max_lengths[j] = max(max_lengths[j],len(record[i][j])+5)
            
    for i in range(len(record)):
        for j in range(3):
            print(f'{record[i][j]:^{max_lengths[j]}}',end='')
        print()
    print()