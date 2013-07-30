import sys
import os

# Hack to set the proper sys.path. Overcomes the export PYTHONPATH pain.
sys.path[:] = map(os.path.abspath, sys.path)
sys.path.insert(0, os.path.abspath(os.getcwd()))

from unittest import TestCase, main

from mucrypt.identity import Identity

class TestIdentity(TestCase):
    def setUp(self):
        pass

    def init_id_file(self):
        self.identity = Identity()
        self.identity.write_identity_file('testing.out')
        with open('testing.out') as f:
            print ''.join(f.readlines())

    def test_initialize_identity(self):
        self.init_id_file()

    def test_read_identity(self):
        self.init_id_file()
        before_private_key = long(self.identity.private_key)
        
        self.identity.import_identity_file('testing.out')
        after_private_key = self.identity.private_key

        self.assertTrue(before_private_key == after_private_key)

if __name__ == '__main__':
    main()
