#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""knit Python/R Markdown and Jupyter, create Pandoc-Flavored Markdown

Usage:
  pymd-knit [-k|--kernel <kernel>] [-m|--mtype <mtype>] <file>
  pymd-knit [-l|--list]
  pymd-knit [-h|--help] [-v|--version]

Arguments:
  <file>  source filename

Options:
  -k,--kernel <kernel>  Jupyter kernel name
  -m,--mtype <mtype>    markdown type (latex(default) or beamer or beamer169)
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
	ctype = 'knit'
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
	kernel = idata[ctype]['default_kernel']
	mtype = idata[ctype]['default_mtype']
	highlight = idata['syntax_highlight']
	if len(args['--kernel']) > 0:
		kernel = args['--kernel'][-1]
	if len(args['--mtype']) > 0:
		mtype = args['--mtype'][-1]
	ibname = ibase.split('.')
	if len(ibname) == 3:
		kernel = ibname[1]
		mtype = ibname[2]
	elif len(ibname) == 2:
		if ibname[1] in pymd.mtypes.keys():
			mtype = ibname[1]
		else:
			kernel = ibname[1]
	if mtype not in pymd.mtypes.keys():
		print("indicate mtype(markdown type) from below:")
		for k, v in pymd.mtypes.items():
			print("  %s: %s" % (k, v))
		exit(-1)
	oext = idata[ctype]['output_types'][0]
	ofile = os.path.join(os.path.dirname(ifile), ibase + "." + oext)
	base = pymd.pymdBase(ifile, ofile, kernel, iext, mtype, highlight)
	base.knit()
	return
