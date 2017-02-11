#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from . chunks import pymdChunk


def get_pymdReader(rtype, infile):
	if rtype == 'pymd':
		return pymdReaderPythonMarkdown(infile)
	elif rtype == 'Rmd':
		return pymdReaderRMarkdown(infile)
	else:
		raise Exception("Incorrect reader type")


class pymdReader(object):
	code_begin = re.compile('')
	doc_begin = re.compile('')

	def __init__(self, source):
		self.source = source
		return

	def read_file(self, source=None):
		if source is None:
			rf = open(self.source, 'rt')
		else:
			rf = open(source, 'rt')
		raw = rf.readline()
		while raw:
			yield raw.strip("\n\r")
			raw = rf.readline()
		rf.close()
		return

	def read(self):
		contents = list()
		is_code = False
		n_code = 0
		n_document = 1
		chunk = pymdChunk('document', "", n_document)
		contents.append(chunk)
		for line in self.read_file():
			if is_code is False and self.code_begin.match(line):
				is_code = True
				n_code += 1
				options = self.code_begin.findall(line)
				if len(options) > 0:
					options = options[0].strip()
				else:
					options = ''
				chunk = pymdChunk('code', options, n_code)
				if chunk.options['source'] is not False:
					for sline in self.read_file(chunk.options['source']):
						chunk.add_content(sline)
				contents.append(chunk)
			elif is_code is True and self.doc_begin.match(line):
				is_code = False
				n_document += 1
				chunk = pymdChunk('document', "", n_document)
				contents.append(chunk)
			else:
				chunk.add_content(line)
		return contents


class pymdReaderPythonMarkdown(pymdReader):
	def __init__(self, source):
		super().__init__(source)
		begin_pattern = '^[`~]{3,}\s*\{\s*[pP]ython(?:(?:\s*,|\s+)(.*)|)\}\s*$'
		end_pattern = '^[`|~]{3,}\s*$'
		self.code_begin = re.compile(begin_pattern)
		self.doc_begin = re.compile(end_pattern)


class pymdReaderRMarkdown(pymdReader):
	def __init__(self, source):
		super().__init__(source)
		begin_pattern = '^[`~]{3,}\s*\{\s*[rR](?:(?:\s*,|\s+)(.*)|)\}\s*$'
		end_pattern = '^[`|~]{3,}\s*$'
		self.code_begin = re.compile(begin_pattern)
		self.doc_begin = re.compile(end_pattern)
