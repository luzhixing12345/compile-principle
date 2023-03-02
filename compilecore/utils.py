

def print_set(name ,table):
    print(name)
    max_str_length = max(len(s) for s in table.keys()) + 1
    for key, value in table.items():
        print(f'   {key:<{max_str_length}}: {str(value)}')
    print()