from os import path

import setuptools

requirements_file = path.join("requirements", "base.in")

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(requirements_file) as rfh:
    contents = rfh.read()
    requirements = contents.strip().split("\n")

setuptools.setup(
    author="CraveFood",
    author_email="devops@cravehq.com",
    license="BSD license",
    name="celery-logger",
    version="0.0.1",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python library for logging celery events",
    install_requires=requirements,
    keywords="logging, celery",
    long_description=long_description,
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    python_requires=">=3.7",
    url="https://github.com/CraveFood/celery-logger",
)
