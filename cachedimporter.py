"""
CachedImporter is a `finder` object that caches the directory
listings of folders on the Python path as it discovers them.

This can reduce the start-up time of scripts and applications that
import a large number of modules.

See PEP 302 (http://www.python.org/dev/peps/pep-0302/) for more info.
"""
import imp
import sys
import os


class CachedImporter(object):

    def __init__(self):
        self.__listdir_cache = {}
        self.__loader_cache = {}

    @classmethod
    def register(cls):
        """registers the CachedImporter with the python import system"""
        finder = cls()
        sys.meta_path.insert(0, finder)

    @classmethod
    def unregister(cls):
        """unregisters the CachedImporter from the python import system"""
        for finder in list(sys.meta_path):
            if isinstance(finder, cls):
                sys.meta_path.remove(finder)

    @classmethod
    def registered_loader(cls):
        """return the loader registered in the the python import system, or None"""
        for finder in list(sys.meta_path):
            if isinstance(finder, cls):
                return finder

    def find_module(self, fullname, path=None):
        """
        CachedImporter replacement of Python's imp.find_module function.
        """
        modulename = fullname.split(".")[-1]
        if modulename != fullname and path is None:
            return None

        for path in path or sys.path:
            contents = self.__listdir(path)

            # check if it's a package
            if modulename in contents:
                pkg_path = os.path.join(path, modulename)
                pkg_contents = self.__listdir(pkg_path)
                for suffix, mode, type_ in imp.get_suffixes():
                    filename = "__init__" + suffix
                    if filename in pkg_contents:
                        description = ("", "", imp.PKG_DIRECTORY)
                        loader = CachedLoader(fullname, pkg_path, description)
                        self.__loader_cache[fullname] = loader
                        return loader

            for suffix, mode, type_ in imp.get_suffixes():
                filename = modulename + suffix
                if filename in contents:
                    pathname = os.path.join(path, filename)

                    # check for a cached file in __pycache__
                    if type_ == imp.PY_SOURCE and "__pycache__" in contents:
                        cachedir = os.path.join(path, "__pycache__")
                        cache_contents = self.__listdir(cachedir)
                        cachedname = ".".join((modulename, imp.get_tag(), "pyc"))
                        if cachedname in cache_contents:
                            cachedpath = os.path.join(cachedir, cachedname)
                            if os.stat(cachedpath).st_mtime >= os.stat(pathname).st_mtime:
                                loader = CachedLoader(fullname, cachedpath, (".pyc", "rb", imp.PY_COMPILED))
                                self.__loader_cache[fullname] = loader
                                return loader

                    loader = CachedLoader(fullname, pathname, (suffix, mode, type_))
                    self.__loader_cache[fullname] = loader
                    return loader

    def is_cached(self, fullname):
        """return True if the module has been cached"""
        return fullname in self.__loader_cache

    def __listdir(self, path):
        """return a cached set of files and directories in `path`"""
        try:
            return self.__listdir_cache[path]
        except KeyError:
            pass

        if not os.path.exists(path) or not os.path.isdir(path):
            self.__listdir_cache[path] = contents = set()
            return contents

        self.__listdir_cache[path] = contents = set(os.listdir(path))
        return contents


class CachedLoader(object):

    def __init__(self, fullname, filename, description):
        self.fullname = fullname
        self.filename = filename
        self.description = description

    def load_module(self, fullname):
        assert fullname == self.fullname
        (suffix, mode, type_) = self.description
        if type_ == imp.PKG_DIRECTORY:
            module = imp.load_module(fullname, None, self.filename, (suffix, mode, type_))
        else:
            with open(self.filename, mode) as fh:
                module = imp.load_module(fullname, fh, self.filename, (suffix, mode, type_))
        module.__loader__ = self
        return module


def register():
    """register the CachedImporter with the python import system"""
    CachedImporter.register()
