

from .base import Core

class Derviation(Core):
    
    def __init__(self, file_path='') -> None:
        super().__init__(file_path)
        self.left_most = False
        self.right_most = False
        
    