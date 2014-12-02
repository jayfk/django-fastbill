#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

try:
    long_description = open('README.md', 'r').read()
except IOError:
    long_description = "fastbill"

setup(
    name='django-fastbill',
    version="0.2.7",
    description='A reusable django app for fastbill integration',
    long_description=long_description,
    author='Jannis Gebauer',
    author_email='ja.geb@pricemesh.io',
    url='http://github.com/jayfk/django-fastbill',
    license='MIT License',
    packages=['django_fastbill', "django_fastbill.management.commands", "django_fastbill.migrations"],
    install_requires=[
        'requests', 'fastbill'
    ],
    setup_requires=["nose>=1.0", "httpretty==0.6.3"],
    test_suite="nose.collector",
    keywords='fastbill api'
)