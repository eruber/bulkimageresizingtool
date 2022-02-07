from setuptools import setup

from version import VERSION

setup(
    name='birt',
    version=VERSION,
    py_modules=['birt', 'cli', 'version'],
    install_requires=[
        'Click',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'birt = cli:cli',
        ],
    },
)
