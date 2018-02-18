#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup



try:
    with open('requirements.txt') as reqs:
        lines = reqs.read().split('\n')
        requirements = list(filter(lambda l: not l.startswith('#') and not l.startswith('git+'), lines))
except IOError:
    requirements = []

try:
    with open('requirements_dev.txt') as test_reqs:
        lines = test_reqs.read().split("\n")[1:]  # skip first line
        test_requirements = list(filter(lambda l: not l.startswith('#') and not l.startswith('git+'), lines))
except IOError:
    test_requirements = []

setup(
    name='lambda_requests',
    version='0.1.1',
    description="Use Requests to invoke AWS Lambdas",
    author="Ilya Sukhanov",
    author_email='ilya@sukhanov.net',
    url='https://github.com/IlyaSukhanov/lambda_requests',
    packages=[
        'lambda_requests',
    ],
    package_dir={'lambda_requests':
                 'lambda_requests'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='lambda_requests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
