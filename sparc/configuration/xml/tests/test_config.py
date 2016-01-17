"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.configuration.xml

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('config.txt',
                     package=sparc.configuration.xml),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')