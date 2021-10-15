from distutils.core import setup
from setuptools import find_packages

setup(
    name='dashy',
    version='0.1dev',
    author='Johan Doe',
    author_email='some.person@email.com',
    packages=find_packages(),
    install_requires=[
        'dash >= 1.1.1',
        'dash-bootstrap-components >= 0.7.0',
        'libsass >= 0.19.2'
    ],
    include_package_data=True
)
