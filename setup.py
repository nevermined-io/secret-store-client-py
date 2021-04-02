#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['requests~=2.21.0']

setup_requirements = ['pytest-runner']

test_requirements = ['pytest']

# Possibly required by developers of nevermined-sdk-py:
dev_requirements = [
    'bumpversion',
    'pkginfo',
    'twine',
    'watchdog',
]

setup(
    author="nevermined-io",
    author_email='root@nevermined.io',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="🐳 Python client for Parity Secret Store.",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='nevermined-secret-store',
    name='nevermined-secret-store',
    packages=find_packages(include=['secret_store_client']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nevermined-io/secret-store-client-py',
    version='0.1.1',
    zip_safe=False,
)
