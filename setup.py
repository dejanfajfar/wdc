from setuptools import setup

version_file = open('version')
version = version_file.read().strip()

setup(
    name='wdc',
    version=version,
    packages=['wdc'],
    entry_points={
        'console_scripts': ['wdc = wdc.runner:cli']
    },

    author='Dejan Fajfar',
    author_email='dejan@fajfar.com',
    url='https://github.com/dejanfajfar/wdc',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ]
)
