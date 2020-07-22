import os

from setuptools import setup
from setuptools.dist import Distribution

# The version number is provided in the version file
version_file = open('version')
version = version_file.read().strip()

# This can be overridden by a special environment variable used in the build process
env_version = os.environ.get('WDC_VERSION')
if env_version is not None and env_version != '':
    version = env_version

# Read readme file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


setup(
    name='wdc',
    version=version,
    packages=[
        'wdc',
        'wdc.helper',
        'wdc.controller'
    ],
    entry_points={
        'console_scripts': ['wdc = wdc.runner:cli']
    },
    long_description=long_description,
long_description_content_type='text/markdown',

    author='Dejan Fajfar',
    author_email='dejan@fajfar.com',
    url='https://github.com/dejanfajfar/wdc',

    include_package_data=True,
    distclass=BinaryDistribution,
    install_requires=[
        'click',
        'termtables'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ]
)
