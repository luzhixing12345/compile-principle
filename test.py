
import unittest
import os
from src.chapter2 import CFGCore

class TestChapter2(unittest.TestCase):

    def test_files(self):

        files = os.listdir('./src/chapter2/testfiles')
        for file in files:
            file_path = os.path.join('./src/chapter2/testfiles',file)
            CFGCore(file_path)



if __name__ == "__main__":
    unittest.main()
