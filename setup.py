#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="lambda_requests",
    version="0.9",
    description="Use Requests to invoke AWS Lambdas",
    author="Ilya Sukhanov",
    author_email="ilya@sukhanov.net",
    url="https://github.com/IlyaSukhanov/lambda-requests",
    packages=[
        "lambda_requests",
    ],
    package_dir={"lambda_requests": "lambda_requests"},
    include_package_data=True,
    install_requires=[
        "boto3",
        "requests",
    ],
    extras_require={
        "testing": [
            "pip~=20.3",
            "flake8",
            "tox",
            "coverage",
            "pytest",
            "pyflakes",
            "pytest-cov",
            "bandit",
            "black~=21.5b1",
            "isort",
            "wheel",
            "twine",
        ],
    },
    license="MIT license",
    zip_safe=False,
    keywords="lambda_requests",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
)
