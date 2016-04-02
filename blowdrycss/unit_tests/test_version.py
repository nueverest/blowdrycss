# python 2
from __future__ import absolute_import

# builtins
from unittest import TestCase, main

# custom
import version

__author__ = 'chad nelson'
__project__ = 'blowdrycss'


class TestTiming(TestCase):
    def test_author(self):
        self.assertIsNotNone(version.__author__)

    def test_project(self):
        self.assertIsNotNone(version.__project__)

    def test_version(self):
        self.assertIsNotNone(version.__version__)

    def test_release(self):
        self.assertIsNotNone(version.__release__)


if __name__ == '__main__':
    main()
