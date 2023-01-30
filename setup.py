#!/usr/bin/env python3
#
#  IRIS Source Code
#  IRIS Client API Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import pathlib

import setuptools

# The directory containing this file
CURR_DIR = pathlib.Path(__file__).parent

# The text of the README file
README = (CURR_DIR / "README.md").read_text()

setuptools.setup(
     name='dfir_iris_client',
     version='1.0.4',
     packages=['dfir_iris_client', 'dfir_iris_client.helper', 'dfir_iris_client.tests'],
     author="DFIR-IRIS",
     author_email="contact@dfir-iris.org",
     description="Client for DFIR-IRIS API",
     long_description=README,
     long_description_content_type="text/markdown",
     url="https://github.com/dfir-iris/dfir-iris-client",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
         "Operating System :: OS Independent",
     ],
     install_requires=[
        'requests',
        'packaging',
        'deprecated'
    ]
 )
