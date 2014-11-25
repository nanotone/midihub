import sys

from setuptools import setup, find_packages


requires = ['rtmidi-python==0.2.2']

if sys.version_info[:2] == (2, 6):
    # For python2.6 we have to require argparse since it
    # was not in stdlib until 2.7.
    requires.append('argparse>=1.1')

setup(
    name='midihub',
    version='0.0.1',
    author='nanotone',
    author_email='nanotone@gmail.com',
    url='https://github.com/nanotone/midihub',
    description="Real-time extensible MIDI routing",
    license='MIT License',
    install_requires=requires,
    packages=find_packages(),
    scripts=['bin/midihub'],
)
