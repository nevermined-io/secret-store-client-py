#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

requirements = [
    'requests',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Ocean Protocol team",
    author_email='devops@oceanprotocol.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="🐳 Python client for Parity Secret Store.",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='secret-store-client',
    name='secret-store-client',
    packages=find_packages(include=['secret_store_client']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/oceanprotocol/secret-store-client-py',
    version='0.0.1',
    zip_safe=False,
)
