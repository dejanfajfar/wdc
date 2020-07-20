import os

from setuptools import setup

# The version number is provided in the version file
version_file = open('version')
version = version_file.read().strip()

# This can be overridden by a special environment variable used in the build process
env_version = os.environ.get('WDC_VERSION')
if env_version is not None and env_version != '':
    version = env_version


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
