#!/usr/bin/env python
#
# Copyright (c) 2023 Superpowered AI All right reserved.
#

import os

import setuptools

long_desc = """# Superpowered AI
LLM-powered autonomous agent with hierarchical task management
"""

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="task-tree-agent",
    version="0.0.1",
    description="Task Tree Agent",
    license="MIT License",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://superpowered.ai",
    project_urls={
        "Homepage": "https://superpowered.ai",
        "Documentation": "https://superpowered.ai/docs",
        "Contact": "https://superpowered.ai/contact/",
    },
    author="superpowered",
    author_email="zach@superpowered.ai",
    keywords="Superpowered AI Task Tree Agent",
    packages=setuptools.find_packages(),
    install_requires=read("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
