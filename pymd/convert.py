#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""convert Python/R Markdown <--> Jupyter Notebook

Usage:
  pymd-convert [-o|--output <oext>] <file>
  pymd-convert [-l|--list]
  pymd-convert [-h|--help] [-v|--version]

Arguments:
  <file>  source filename

Options:
  -o,--output <oext>    extension of output filetype
  -l,--list             List filetype
  -h,--help             Show this help
  -v,--version          Show version
"""

import os
import sys
from docopt import docopt, DocoptExit
import pymd


def main():
	try:
		args = docopt(
			__doc__,
			argv=None,
			help=True,
			version=pymd.__version__,
			options_first=False
		)
	except DocoptExit as e:
		print("Invalid arguments or optiions", file=sys.stderr)
		print(e, file=sys.stderr)
		sys.exit(-1)
	except SystemExit:
		sys.exit(0)
	ctype = 'convert'
	if args['--list']:
		pymd.list_types(ctype)
		sys.exit(0)
	ifile = args['<file>']
	if ifile is None:
		print("Indicate source file")
		sys.exit(-1)
	if not os.path.exists(ifile):
		print("Source file(%s) is not exists" % ifile, file=sys.stderr)
		sys.exit(-1)
	ibase, iext = os.path.splitext(os.path.basename(ifile))
	iext = iext.replace(".", "")
	idata = pymd.filetypes.get(iext)
	if idata is None:
		print("Source filetype is not correspond")
		pymd.list_types(ctype)
		sys.exit(-1)
	if not idata[ctype]['input']:
		print("Source filetype is not correnpond in pymd-%s" % ctype)
		sys.exit(-1)
	highlight = idata['syntax_highlight']
	if len(args['--output']) > 0:
		oext = args['--output'][-1]
		if oext not in pymd.mtypes.keys():
			print("Output filetype is not correspond")
			pymd.list_types(ctype)
			exit(-1)
		if oext not in idata[ctype]['output_types']:
			print("Output filetype is not correspond with input filetype")
			pymd.list_types(ctype)
			exit(-1)
	else:
		oext = idata[ctype]['default_output']
	ofile = os.path.join(os.path.dirname(ifile), ibase + "." + oext)
	base = pymd.pymdBase(ifile, ofile, '', iext, oext, highlight)
	base.convert()
	return
