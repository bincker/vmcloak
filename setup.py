#!/usr/bin/env python
# Copyright (C) 2014 Jurriaan Bremer.
# This file is part of VMCloak - http://www.vmcloak.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='VMCloak',
    version='0.1.4',
    author='Jurriaan Bremer',
    author_email='jurriaanbremer@gmail.com',
    packages=[
        'vmcloak',
        'vmcloak.data',
        'vmcloak.data.bootstrap',
        'vmcloak.data.hwconf',
    ],
    scripts=[
        'bin/vmcloak',
        'bin/vmcloak-deps',
        'bin/vmcloak-gethwconf',
        'bin/vmcloak-iptables',
    ],
    url='http://vmcloak.org/',
    license='docs/LICENSE.txt',
    description='Automated Virtual Machine Generation and Cloaking '
                'for Cuckoo Sandbox.',
    install_requires=[
        # Useful when running multiple instances of VMCloak at once.
        'lockfile',

        # Libraries to build the documentation.
        'sphinx',

        # Required on BSD systems for unknown reasons.
        'jinja2',

        # Required for the VBoxRPC virtual machine module.
        'requests',
        'requests-toolbelt',
    ],
)
