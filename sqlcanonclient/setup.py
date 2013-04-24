#!/usr/bin/env python
# setup.py
# Copyright (C) 2009-2013 PalominoDB, Inc.
# 
# You may contact the maintainers at eng@palominodb.com.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from setuptools import setup, find_packages
setup(
    name='sqlcanonclient',
    version='0.1',
    package_dir={'':'src'},
    packages=find_packages('src'),
    dependency_links=[
        'http://sourceforge.net/projects/pylibpcap/files/pylibpcap/0.6.4/pylibpcap-0.6.4.tar.gz/download#egg=pylibpcap-0.6.4'
    ],
    install_requires=[
        'MySQL-python==1.2.4',
        'sqlparse==0.1.6',
        'mmh3==2.0',
        'construct==2.06',
        'pylibpcap==0.6.4'],
    entry_points={
        'console_scripts': [
            'sqlcanonclient = sqlcanonclient.sqlcanonclient:main',
        ]
    }
    #scripts=[
    #    'src/sqlcanonclient/sqlcanonclient.py',
    #],
)
