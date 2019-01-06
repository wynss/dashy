from distutils.core import setup

setup(
    name='dashy',
    version='0.1dev',
    author='Johan Doe',
    author_email='some.person@email.com',
    packages=['dashy'],
    install_requires=[
        'dash >= 0.35.0',
        'dash-core-components >= 0.42.0',
        'dash-html-components >= 0.13.4',
        'dash-renderer >= 0.16.1',
        'plotly >= 3.4.2'
    ],
    include_package_data=True
)
