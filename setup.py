#!/usr/bin/env python3

from setuptools import setup

setup(name="geppetto-cli",
      version="0.1",
      description="Command line interface to automate control of pneumatic system",
      url="https://github.com/FordyceLab/geppetto-cli",
      author="Tyler Shimko",
      author_email="tshimko@stanford.edu",
      license="MIT",
      packages=["geppetto_cli"],
      install_requires=[
        "pyaml",
        "tqdm",
        "pymodbus3"
      ],
      scripts=['bin/geppetto.py'],
      zip_safe=False)
