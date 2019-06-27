"""
ref2bib
Async script to build a BibTeX database out of reference identifiers
"""
import sys
from setuptools import setup, find_packages
if sys.version_info < (3, 7):
    raise RuntimeError('ref2bib requires Python 3.7+')


short_description = __doc__.split("\n")

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = ("\n".join(short_description[2:]),)


setup(
    # Self-descriptive entries which should always be present
    name="ref2bib",
    author="Jaime Rodríguez-Guerra",
    author_email="jaime.rogue@gmail.com",
    description=short_description[0],
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.1",
    license="MIT",
    py_modules=["ref2bib"],
    # Optional include package data to ship with your package
    # Customize MANIFEST.in if the general case does not suit your needs
    # Comment out this line to prevent the files from being packaged with your software
    include_package_data=True,
    install_requires=["aiohttp", "aiofiles"],
    # platforms=['Linux',
    #            'Mac OS-X',
    #            'Unix',
    #            'Windows'],            # Valid platforms your code works on, adjust to your flavor
    python_requires=">=3.7",  # Python version restrictions
    # Manual control if final package is compressible or not, set False to prevent the .egg from being made
    # zip_safe=False,
    entry_points='''
        [console_scripts]
        ref2bib=ref2bib:main
    '''
)

