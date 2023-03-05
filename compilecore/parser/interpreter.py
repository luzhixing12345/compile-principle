
import textwrap
from .parser import Parser
from .error import Error, InterpreterError
        
class ASTVisitor(object):
    
    def __init__(self, parser) -> None:
        self.parser:Parser = parser
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=circle, fontsize=12, fontname="Courier", height=.1];
          ranksep=.3;
          edge [arrowsize=.5]
        """)]
        self.dot_body = []
        self.dot_footer = ['}']
    
    def visit(self, node):
        # 获取节点类型
        method_name = 'visit_' + type(node).__name__
        # 反射
        visit_method = getattr(self, method_name, self.visit_error)
        return visit_method(node)

    def visit_error(self, node) -> Error:
        s = f'找不到 visit_{type(node).__name__} 方法, 需要编写 {type(node).__name__} 类的对应visit方法'
        raise InterpreterError(s,type(node).__name__)
    
    def error(self, error_code, node) -> Error:
        raise InterpreterError(
            error_code=error_code,
            message=f'{error_code.value} -> {node}',
        )