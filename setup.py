from setuptools import setup, find_packages
from os import path
from foliage import __version__

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(
    name='wagtail-foliage',
    version=__version__,

    packages=find_packages(),
    include_package_data=True,

    description='Utilities for programatically constructing page trees in '
                'Wagtail',

    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/harrislapiroff/wagtail-foliage',

    author='Harris Lapiroff',
    author_email='harris@freedom.press',

    license='BSD-3-Clause',

    install_requires=[
        'typing>=3.6.6',
        'wagtail>=1.11',
    ],

    extras_require={
        'docs': [
            'Sphinx>=1.7',
            'sphinx_rtd_theme>=0.4.0',
        ],
        'test': [
            'tox',
            'pytest>=3.5',
            'pytest-django>=3.2',
            'pytest-pythonpath>=0.7.2',
        ],
    },

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 1',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
