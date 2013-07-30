import sys
import os

# Hack to set the proper sys.path. Overcomes the export PYTHONPATH pain.
sys.path[:] = map(os.path.abspath, sys.path)
sys.path.insert(0, os.path.abspath(os.getcwd()))

from unittest import TestCase, main

from mucrypt.client import MUSession, MUCrypt

class TestMUCrypt(TestCase):
    def setUp(self):
        pass
    
    def test_foo(self):
        pass

if __name__ == '__main__':
    main()
