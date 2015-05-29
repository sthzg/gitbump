import os
from distutils.core import setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gitbump',
    version='0.0.0',
    url='',
    packages=['gitbump'],
    license='',
    author='Stephan Herzog',
    author_email='sthzgvie@gmail.com',
    description='Bump a git tag',
    classifiers=[
    ],
    install_requires=[
        'Click',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        gitbump=gitbump.gitbump:gitbump
    ''',
)
