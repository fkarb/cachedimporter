"""
Unittests for CachedImporter.
"""
from cachedimporter import CachedImporter, CachedLoader
import unittest
import sys


class CachedImporterTests(unittest.TestCase):

    def setUp(self):
        CachedImporter.register()

    def tearDown(self):
        CachedImporter.unregister()

    def test_register(self):
        finder = CachedImporter.registered_loader()
        self.assertTrue(finder is not None)

    def test_finder(self):
        # CachedImporter is the finder and loader.
        # Check the 'cachedimporter' module can be found.
        finder = CachedImporter.registered_loader()
        loader = finder.find_module("cachedimporter")
        self.assertTrue(isinstance(loader, CachedLoader))

    def test_loader(self):
        finder = CachedImporter.registered_loader()
        loader = finder.find_module("cachedimporter")
        module = loader.load_module("cachedimporter")
        self.assertTrue(module.__loader__ is loader)

    def test_import(self):
        # try importing a module that isn't already imported
        self.assertTrue("json" not in sys.modules)
        finder = CachedImporter.registered_loader()
        self.assertFalse(finder.is_cached("json"))

        import json

        self.assertTrue("json" in sys.modules)
        self.assertTrue(finder.is_cached("json"))

    def test_import_package(self):
        # try importing a package that isn't already imported
        self.assertTrue("html.parser" not in sys.modules)
        finder = CachedImporter.registered_loader()
        self.assertFalse(finder.is_cached("html.parser"))

        import html.parser

        self.assertTrue("html.parser" in sys.modules)
        self.assertTrue(finder.is_cached("html.parser"))
