from setuptools import setup

_domaven_version = '0.0.1'

install_requires = [
    'treelib',
    'flake8',
    'pyflakes',
    'mccabe',
    'pep8',
    'dosocs2'
]

tests_require = [
    'pytest'
]

setup(
    name='domaven',
    version=_domaven_version,
    description='Connector between DoSOCSv2 and Maven for relationships',
    long_description='',
    url='https://github.com/tpflueger/CSCI4900',
    author='Tyler Pflueger, Aarjav Chauhan',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 2.7'
        'Environment :: Console'
    ],

    keywords='spdx licenses maven dosocs2',
    packages=['scripts'],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'tests': install_requires + tests_require
    },
    entry_points={'console_scripts': ['domaven=scripts.main:main']},
    test_suite='py.test',

    zip_safe=False
)
