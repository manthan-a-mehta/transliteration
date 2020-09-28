import os

from setuptools import setup, find_packages

__version__ = '0.1'




setup(
    name='transliteration',
    version=__version__,
    description='transliteration',
    url='https://github.com/manthan-kodar/transliteration.git',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    dependency_links=[],
    # install_requires=requirements,
    python_requires=">=3.7"
)