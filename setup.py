#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 14:57:59 2024

@author: erikware
"""

from setuptools import setup, find_packages
import os

def create_folders():
    # Create necessary folders
    folders = ['data', 'logging', 'output']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

create_folders()

setup(
    name='coin_gecko_tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
)
