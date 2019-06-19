from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='diffusionqclib',  # Required
    version='2.0.4',  # Required
    description='Library to support SlicerDiffusionQC module',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    install_requires=['plumbum','nibabel','pynrrd'],
    url='https://github.com/pnlbwh/SlicerDiffusionQC/',
    author="""Tashrif Billah, Isaiah Norton (Brigham & Women's Hospital / Harvard Medical School)""",
    packages=find_packages(),  # Required
)
