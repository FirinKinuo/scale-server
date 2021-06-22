from cx_Freeze import setup, Executable

executables = [Executable('run.py', targetName='weight_comport.exe')]

excludes = ['unicodedata', 'tkinter']

includes = ['dotenv', 'aiohttp', 'jinja2', 'aiohttp_jinja2', 'serial']

zip_include_packages = ["aiohttp", "aiohttp_jinja2", "app", "async_timeout", "asyncio",
                        "attr", "chardet", "collections", "concurrent", "ctypes",
                        "distutils", "dotenv", "email", "encodings", "html",
                        "http", "idna", "importlib", "jinja2", "json",
                        "lib2to3", "logging", "markupsafe", "multidict", "multiprocessing",
                        "pydoc_data", "serial", "test", "tkinter", "unittest",
                        "urllib", "xml", "xmlrpc", "yarl"]

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',

    }
}

setup(name='weight_comport',
      version='1.0.1',
      description='Чтение компорта промышленных весов с отправкой данных по webhook и на табло по компорту',
      executables=executables,
      options=options)
