from distutils.core import setup
from setuptools import find_packages

setup(
    name='dashy',
    version='0.1dev',
    author='Johan Doe',
    author_email='some.person@email.com',
    packages=find_packages(),
    install_requires=[
        'dash >= 0.35.0',
        'dash-core-components >= 0.42.0',
        'dash-html-components >= 0.13.4',
        'dash-renderer >= 0.16.1',
        'plotly >= 3.4.2',
        'libsass >= 0.17.0'
    ],
    include_package_data=True
)
