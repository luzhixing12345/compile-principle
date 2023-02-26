
from .base import Core

class FFS(Core):
    
    def __init__(self, file_path='') -> None:
        super().__init__(file_path)
    
    def calculate_first_set(self):
        ...

    def calculate_follow_set(self):
        ...
        
    def calculate_select_set(self):
        
        ...
        
    def info(self):
        self.parse_grammar()