#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import pymd


def setup_package():
	metadata = dict()
	metadata['name'] = pymd.__package__
	metadata['version'] = pymd.__version__
	metadata['description'] = pymd.description_
	metadata['author'] = pymd.author_
	metadata['url'] = pymd.url_
	metadata['license'] = 'MIT'
	metadata['entry_points'] = {
		'console_scripts': [
			'pymd-knit = pymd.knit:main',
			'pymd-convert = pymd.convert:main',
		],
	}
	metadata['packages'] = find_packages()
	metadata['include_package_data'] = False
	metadata['install_requires'] = [
		'docopt',
		'jupyter',
	]
	setup(**metadata)


if __name__ == "__main__":
	setup_package()
