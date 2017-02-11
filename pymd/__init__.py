from . readers import get_pymdReader
from . processors import get_pymdProcessor
from . writers import get_pymdWriter

__version__ = '0.1.0'
description_ = 'convert python markdown(.pymd) to pandoc flavor markdown(.md)'
url_ = 'https://github.com/tetutaro/pymd'
author_ = 'maruyama'

filetypes = {
	'md': {
		'name': 'Pandoc Flavor Markdown',
		'syntax_highlight': '',
		'knit': {
			'input': False,
			'output_types': [],
			'default_mtype': '',
			'default_kernel': '',
		},
		'convert': {
			'input': False,
			'output_types': [],
			'default_output': '',
		},
	},
	'pymd': {
		'name': 'Python Markdown',
		'syntax_highlight': '.python',
		'knit': {
			'input': True,
			'output_types': ['md'],
			'default_mtype': 'latex',
			'default_kernel': 'python3',
		},
		'convert': {
			'input': True,
			'output_types': ['py'],
			# 'output_types': ['py', 'ipynb'],
			'default_output': 'py',
		},
	},
	'Rmd': {
		'name': 'R Markdown',
		'syntax_highlight': '.r',
		'knit': {
			'input': True,
			'output_types': ['md'],
			'default_mtype': 'latex',
			'default_kernel': 'irkernel33',
		},
		'convert': {
			'input': True,
			'output_types': ['R'],
			# 'output_types': ['R', 'ipynb'],
			'default_output': 'R',
		},
	},
	'py': {
		'name': 'Python Script',
		'syntax_highlight': '',
		'knit': {
			'input': False,
			'output_types': [],
			'default_mtype': '',
			'default_kernel': '',
		},
		'convert': {
			'input': False,
			'output_types': [],
			'default_output': '',
		},
	},
	'R': {
		'name': 'R Script',
		'syntax_highlight': '',
		'knit': {
			'input': False,
			'output_types': [],
			'default_mtype': '',
			'default_kernel': '',
		},
		'convert': {
			'input': False,
			'output_types': [],
			'default_output': '',
		},
	},
	'ipynb': {
		'name': 'Jupyter Notebook',
		'syntax_highlight': '',
		'knit': {
			'input': False,
			# 'input': True,
			'output_types': ['md'],
			'default_mtype': 'latex',
			'default_kernel': 'python3',
		},
		'convert': {
			'input': False,
			# 'input': True,
			'output_types': ['pymd', 'Rmd', 'py', 'R'],
			'default_output': 'pymd',
		},
	},
}

mtypes = {
	'latex': 'Pandoc Flavor Markdown for LaTeX',
	'beamer': 'Pandoc Flavor Markdown for LaTeX beamer(4:3)',
	'beamer169': 'Pandoc Flavor Markdown for LaTeX beamer(16:9)',
}


def list_types(ctype):
	print("pymd-%s converts:" % ctype)
	for iext, idata in filetypes.items():
		if idata[ctype]['input']:
			for oext in idata[ctype]['output_types']:
				iname = idata['name']
				oname = filetypes[oext]['name']
				print("  %s(.%s) -> %s(.%s)" % (iname, iext, oname, oext))
	return


def get_kernel_dict():
	kernel_dict = dict()
	for iext, idata in filetypes.items():
		if idata['knit']['default_kernel'] != '':
			idict = {
				'oext': idata['name'],
				'highlight': idata['syntax_highlight']
			}
			kernel_dict[idata['knit']['default_kernel']] = idict
	return kernel_dict


class pymdBase():
	def __init__(self, ifile, ofile, kernel, itype, mtype, highlight):
		self.reader = get_pymdReader(itype, ifile)
		self.processor = get_pymdProcessor('jupyter', kernel)
		self.writer = get_pymdWriter(mtype, ofile, highlight)
		return

	def __str__(self):
		ret = []
		for i, c in enumerate(self.contents):
			ret.append('Chunk %d (%s):' % (i, c.name))
			ret.append(str(c))
		return '\n'.join(ret)

	def read(self):
		self.contents = self.reader.read()
		return

	def run(self):
		self.processor.run(self.contents)
		return

	def write(self):
		self.writer.write(self.contents)
		return

	def knit(self):
		self.read()
		self.run()
		self.write()
		return

	def convert(self):
		self.read()
		self.write()
		return
