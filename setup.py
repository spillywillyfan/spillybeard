import codecs
import os

import setuptools


def read(filename):
    """Read and return `filename` in root dir of project and return string."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, filename), "r") as openfile:
        return openfile.read()


setuptools.setup(
    name="spillybeard",
    version="0.0.1",
    description="Add SpillyBeards to photos of cute frens.",
    long_description=read("README.md"),
    packages=setuptools.find_packages(),
    package_data={
        "static": ["README.md"],
    },
    install_requires=[
        "click",
        "face-recognition",
    ],
    license=read("LICENSE"),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        spillybeard=spillybeard.cli:entry_point
    """,
)
