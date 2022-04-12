from pkg_resources import parse_requirements
from setuptools import setup

NAME = "Scale Server"
VERSION = '2.4.3'
DESCRIPTION = 'Handler of weights of various companies for exchange with 1C by HTTP'
MODULES = ['app', 'app.web', 'app.scales', 'app.scales.ethernet', 'app.scales.ethernet.massak',
           'app.scales.scale_serial', 'app.settings']


def load_requirements(filename: str) -> list:
    with open(file=filename, mode='r', encoding="utf-8") as file:
        return [f"""{req.name}{f"[{','.join(req.extras)}]" if req.extras else ''}{req.specifier}"""
                for req in parse_requirements(file.read())]


setup(
    name=NAME,
    version=VERSION,
    packages=MODULES,
    url='https://github.com/FirinKinuo/scale-server',
    license='GPL-3.0',
    author='fkinuo',
    author_email='deals@fkinuo.ru',
    description=DESCRIPTION,
    install_requires=load_requirements(filename='requirements.txt'),
    entry_points={
        'console_scripts': [
            'scale_server = app.__main__',
        ]
    },
    include_package_data=True
)
