
from .base import Core

class FFS(Core):
    
    def __init__(self, file_path='') -> None:
        super().__init__(file_path)
    
    def get_first_set(self):
        ...
        

    def get_follow_set(self):
        ...
        
    def get_select_set(self):
        
        ...
        
    def info(self):
        print(self.epsilon)