# cachedimporter
CachedImporter is an import hook that caches the directory
listings of folders on the Python path as it discovers them.

This can reduce the start-up time of scripts and applications that
import a large number of modules.

See PEP 302 (http://www.python.org/dev/peps/pep-0302/) for more info.

Usage:

```python
  import cachedimporter
  cachedimporter.register()
```
