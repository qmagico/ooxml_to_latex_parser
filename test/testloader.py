# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

import unittest
import sys
import os

PROJECT_PATH = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-2])
sys.stderr = open(os.devnull, 'w')
if __name__ == '__main__':

    sys.path.insert(0, os.path.join(PROJECT_PATH, 'src', 'ooxml_to_latex'))

    tests = unittest.TestLoader().discover(PROJECT_PATH, "*tests.py")

    result = unittest.TextTestRunner().run(tests)

    for skipped in result.skipped:
        print skipped

    if not result.wasSuccessful():
        sys.exit(1)

