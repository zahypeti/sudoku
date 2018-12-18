import setuptools


setuptools.setup(
    name="sudoku",
    author="Peter Zahemszky",
    author_email="29452238+pzahemszky@users.noreply.github.com",
    # Requirements installed by `python setup.py install`
    install_requires=["numpy >= 1.14.2"],
    # Test run by `python setup.py test`
    test_suite="sudoku.tests",
)
