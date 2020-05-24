#!/usr/bin/python3

from setuptools import setup, find_packages

requirements = open("requirements.txt").read()

setup(
    name="task_progress_api",
    version="0.0.1",
    description="Elasticsearch re-indexing tasks tracking tool",
    author="ahmadimt",
    author_email="ahmad.imt07@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
