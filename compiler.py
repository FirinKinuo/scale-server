import sys
from sys import path as sys_path
from os import path

from cx_Freeze import setup, Executable

from setup import (
    NAME,
    VERSION,
    DESCRIPTION,
    MODULES,
    load_requirements
)

executables = [Executable('app.__main__.py', targetName='weight_comport.exe')]

excludes = ['unicodedata', 'tkinter']

includes = MODULES + load_requirements('requirements.txt')

zip_include_packages = ["aiohttp", "aiohttp_jinja2", "app", "async_timeout", "asyncio",
                        "attr", "chardet", "collections", "concurrent", "ctypes",
                        "distutils", "email", "encodings", "html",
                        "http", "idna", "importlib", "jinja2", "json",
                        "lib2to3", "logging", "markupsafe", "multidict", "multiprocessing",
                        "pydoc_data", "scale_serial", "urllib", "xml", "xmlrpc", "yarl", 'requests']

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'include_files': include_dirs,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',

    }
}

if sys.platform.startswith('linux'):
    executables = [Executable('__main__.py', targetName='weight_comport')]
    options['build_exe']['build_exe'] = 'build_linux'

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      executables=executables,
      options=options)
