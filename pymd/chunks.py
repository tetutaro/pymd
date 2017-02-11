#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from copy import deepcopy


class pymdChunk():
	default_options = {
		"echo": True,
		"evaluate": True,
		"label": False,
		"name": False,
		"caption": False,
		"source": False,
		"figsize": (6, 4),
		"tabs": 4,
	}

	def __init__(self, chunk_type, options, n=0):
		self.chunk_type = chunk_type
		self.offset = n
		self.contents = []
		self.options = deepcopy(self.default_options)
		self.pass_options = list()
		self.results = []
		self.pending_texts = []
		self.num_image = 0
		self.error = None
		options = options.strip()
		if len(options) > 0:
			for i, topt in enumerate(options.split(',')):
				if i == 0 and "=" not in topt:
					topt = 'name="%s"' % topt
				elif "=" not in topt:
					self.pass_options.append(topt.strip())
					continue
				k, v = (t.strip() for t in topt.split("=")[:2])
				v = eval(v)
				if k in list(self.options.keys()):
					self.options[k] = v
				else:
					self.pass_options.append(topt.strip())
		if self.options['name'] is False:
			if self.options['label'] is not False:
				self.name = self.options['label']
			else:
				self.name = "%s%d" % (self.chunk_type, self.offset)
		else:
			self.name = self.options['name']
		if self.options['source'] is not False:
			if self.options['caption'] is False:
				self.options['caption'] = self.options['source']
			if self.options['label'] is False:
				self.options['label'] = self.options['source']
		return

	def __str__(self):
		ret = []
		ret.append('  chunk_type: %s' % self.chunk_type)
		ret.append('  offset: %d' % self.offset)
		ret.append('  options:')
		for k, v in self.options.items():
			ret.append('    {k}: {v}'.format(k=k, v=v))
		ret.append('  contents:')
		for c in self.contents:
			ret.append('    %s' % c)
		return "\n".join(ret)

	def add_content(self, line):
		if self.chunk_type == 'code':
			self.contents.append(line.replace("\t", " " * self.options['tabs']))
		else:  # self.chunk_type == 'docuemnt'
			self.contents.append(line)
		return
