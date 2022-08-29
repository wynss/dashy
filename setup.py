from distutils.core import setup
from setuptools import find_packages

setup(
    name='dashy',
    version='0.1dev',
    author='Johan Doe',
    author_email='some.person@email.com',
    packages=find_packages(),
    install_requires=[
        'dash >= 2.6.1',
        'dash-bootstrap-components >= 1.2.1',
        'libsass >= 0.21.0'
    ],
    include_package_data=True
)
