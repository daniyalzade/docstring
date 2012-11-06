from distutils.core import setup
import docstring

requires = []

packages = [
    'docstring',
]

setup(
    name='docstring',
    author='Eytan Daniyalzade',
    author_email='eytan@chartbeat.com',
    url='http://chartbeat.com',
    packages=packages,
    description='Decorators for auto-generating HTML response for API endpoints',
    long_description=open('README.rst').read(),
    version=docstring.__version__,
    data_files=[
        ('', ['README.rst', 'LICENSE']),
        ('docstring', [
            'docstring/base.html',
            'docstring/style.css',
            ]),
        ],
    package_dir={
        'docstring': 'docstring'
        },
    package_data={
        'docstring': [
            '*.html',
            '*.css',
            ],
        },
    license=open('LICENSE').read(),
    install_requires=requires,
    include_package_data=True,
)
