import os
from .grammar import CFG


class CFGCore:
    def __init__(self, file_path) -> None:
        if not os.path.exists(file_path):  # pragma: no cover
            raise FileNotFoundError(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read().split("\n")

        if len(file_content) == 0:  # pragma: no cover
            raise ValueError("文件内容为空")
        self.grammar = CFG()
        self.parse_grammar(file_content)

    def parse_grammar(self, file_content):
        for i in range(len(file_content)):
            line: str = file_content[i]
            if len(line) == 0 or line[0] == '#': # 忽略注释行和空行
                continue
            production = line.split("->")
            if len(production) != 2:  # pragma: no cover
                raise ValueError(f"产生式 [{production}] 不符合规范, 应以 -> 分隔")

            production_head = production[0].strip()
            production_bodys = production[1].split("|")

            if i == 0:
                self.grammar.begin_symbol = production_head  # 起始符号
            if len(production_head) != 1: # pragma: no cover
                raise ValueError(f'产生式左侧非终结符应为单个字符')

            if self.grammar.productions.get(production_head) is None:
                self.grammar.productions[production_head] = []
            # 展开所有产生式

            for production_body in production_bodys:
                production_body = production_body.strip()
                if (
                    self.grammar.epsilon in production_body and len(production_body) != 1
                ):  # pragma: no cover
                    raise ValueError(f"产生式 {production_body} 中不应出现 {self.grammar.epsilon}")

                self.grammar.productions[production_head].append(production_body)

        self.grammar.parse()
        self.grammar.info()
        self.grammar.show_productions()
