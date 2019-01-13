import setuptools


TROVE_CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Games/Entertainment :: Puzzle Games",
]

SHORT_DESCRIPTION = "A platform independent sudoku solver written in Python 3."


with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="pZudoku",
    version="0.1.0",

    # Short description used by `pip`
    description=SHORT_DESCRIPTION,
    # Long description used on PyPI
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/pzahemszky/pZudoku",
    author="Peter Zahemszky",
    author_email="29452238+pzahemszky@users.noreply.github.com",

    # "Trove classifiers" used by PyPI searches
    classifiers=TROVE_CLASSIFIERS,
    keywords='sudoku sudoku-solver',

    packages=setuptools.find_packages(exclude=['tests']),

    # Requirements installed by `python setup.py install`
    install_requires=[
        # pip 9.0.0 notifies about python_requires incompatibility
        "pip >= 9.0.0",
        # setuptools 38.6.0 introduces long_description_content_type
        "setuptools >= 38.6.0",
        # NumPy 1.8.0 introduces np.full()
        "numpy >= 1.8.0",
    ],

    python_requires=">=3.4",
    tests_require=["flake8 >= 3.4", "coverage >= 4.5.2", "codecov"],

    project_urls={
        "Tracker": "https://github.com/pzahemszky/pZudoku/issues",
    },

    # Test run by `python setup.py test`
    test_suite="pZudoku.tests",
)
