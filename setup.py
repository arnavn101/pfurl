from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name='pfurl',
    python_requires='>=3.5',
    version='2.2.2.2',
    description='(Python) Path-File URL comms',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author='Rudolph Pienaar',
    author_email='rudolph.pienaar@gmail.com',
    url='https://github.com/FNNDSC/pfurl',
    packages=['pfurl'],
    install_requires=['pycurl~=7.43.0.5', 'pfmisc==1.4.0', 'colorama>=0.4.3'],
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/pfurl'],
    license='MIT',
    zip_safe=False
)
