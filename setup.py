from setuptools import setup

setup(
    name="wdc",
    version="0.1",
    packages=['wdc'],
    entry_points={
        "console_scripts": ['wdc = wdc.runner:cli']
    },

    author='Dejan Fajfar',
    author_email='dejan@fajfar.com',
    url='https://github.com/dejanfajfar/wdc'
)
