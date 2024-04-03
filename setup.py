from setuptools import find_packages, setup
from typing import List
import setuptools

import os

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "0.0.1"

REPO_NAME = "Py_Projects"
AUTHER_USER_NAME = "trehansalil"
SRC_REPO = "textSummarizer"
AUTHER_EMAIL = "trehansalil1@gmail.com"

setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHER_USER_NAME,
    author_email=AUTHER_EMAIL,
    description= "A Small app for news summarization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHER_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHER_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"", "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],
)