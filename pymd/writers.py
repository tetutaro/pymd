#!/usr/bin/env python3
# -+- coding:utf-8 -*-

import base64
import re

theader = re.compile("<thead>(.*?)</thead>")
tbody = re.compile("<tbody>(.*?)</tbody>")
trows = re.compile("<tr.*?>(.*?)</tr>")
tcells = re.compile("<t[d|h].*?>(.*?)</t[d|h]>")
ansi = re.compile("\x1b\\[(.*?)([@-~])")


def get_pymdWriter(wtype, dest, highlight):
	if wtype == 'latex':
		return pymdWriterLaTeX(dest, highlight)
	elif wtype in ['beamer', 'beamer169']:
		return pymdWriterBeamer(dest, highlight)
	elif wtype == 'py':
		return pymdWriterPython(dest, highlight)
	elif wtype == 'R':
		return pymdWriterR(dest, highlight)
	else:
		raise Exception("Incorrect writer type")


class pymdWriter(object):
	def __init__(self, dest, highlight):
		self.dest = dest
		self.syntax_highlight = highlight
		return

	def pre_code(self, chunk):
		pass

	def post_code(self, chunk):
		pass

	def pre_error(self, chunk):
		pass

	def post_error(self, chunk):
		pass

	def pre_image(self, chunk, offset):
		pass

	def post_image(self, chunk, offset):
		pass

	def pre_table(self, chunk):
		pass

	def post_table(self, chunk):
		pass

	def pre_text(self, chunk):
		pass

	def post_text(self, chunk):
		pass

	def write_image(self, chunk, data, offset):
		if offset == 1 and chunk.num_image == 1:
			offset = 0
		self.pre_image(chunk, offset)
		if offset == 0:
			image_fname = chunk.name + ".png"
		else:
			image_fname = "%s_%d.png" % (chunk.name, offset)
		if chunk.options['caption'] is False:
			image_caption = ''
		elif offset == 0:
			image_caption = chunk.options['caption']
		else:
			image_caption = chunk.options['caption'] + "（%d）" % offset
		if chunk.options['label'] is False:
			image_label = ''
		elif offset == 0:
			image_label = '{#fig:%s}' % chunk.options['label']
		else:
			image_label = '{#fig:%s_%d}' % (chunk.options['label'], offset)
		wb = open(image_fname, "wb")
		wb.write(base64.b64decode(data))
		wb.close()
		tag = "![{image_caption}]({image_fname}){image_label}\n".format(**locals())
		self.wf.write(tag)
		self.post_image(chunk, offset)
		return

	def write_table(self, chunk, data):
		self.pre_table(chunk)
		tdata = data.replace("\n", "")
		header = theader.findall(tdata)[0]
		body = tbody.findall(tdata)[0]
		header_rows = trows.findall(header)
		body_rows = trows.findall(body)
		header_cells = list()
		max_columns = 0
		for t in header_rows:
			cells = [x.strip() for x in tcells.findall(t)]
			if len(cells) > max_columns:
				max_columns = len(cells)
			header_cells.append(cells)
		body_cells = list()
		for t in body_rows:
			cells = [x.strip() for x in tcells.findall(t)]
			if len(cells) > max_columns:
				max_columns = len(cells)
			body_cells.append(cells)
		for t in header_cells:
			self.wf.write("| " + " | ".join(t) + " |\n")
		self.wf.write("| " + " | ".join([":---:"] * max_columns) + " |\n")
		for t in body_cells:
			self.wf.write("| " + " | ".join(t) + " |\n")
		self.post_table(chunk)
		return

	def write_text(self, chunk, data):
		chunk.pending_texts.append(data.strip())
		return

	def write_pending_texts(self, chunk):
		self.pre_text(chunk)
		data = "\n".join(chunk.pending_texts)
		self.wf.write(data.strip().replace("\n", "\\\n") + "\n")
		self.post_text(chunk)
		return

	def bind_result(self, chunk, data):
		if "image/png" in data:
			self.write_image(chunk, data["image/png"], data["image_offset"])
		elif "text/html" in data:
			self.write_table(chunk, data["text/html"])
		elif chunk.num_image == 0:
			self.write_text(chunk, data["text/plain"])
		return

	def write_code(self, chunk):
		if chunk.options["echo"]:
			self.pre_code(chunk)
			self.wf.write("\n".join(chunk.contents) + "\n")
			self.post_code(chunk)
		if chunk.error is not None:
			self.pre_error(chunk)
			error_message = ansi.sub('', chunk.error.strip())
			self.wf.write(error_message.replace("\n", "\\\n") + "\n")
			self.post_error(chunk)
		for data in chunk.results:
			self.bind_result(chunk, data)
		if len(chunk.pending_texts) > 0:
			self.write_pending_texts(chunk)
		return

	def write_document(self, chunk):
		self.wf.write("\n".join(chunk.contents))
		return

	def write(self, contents):
		self.wf = open(self.dest, "wt")
		for chunk in contents:
			if chunk.chunk_type == 'code':
				self.write_code(chunk)
			else:
				self.write_document(chunk)
		self.wf.close()
		return


class pymdWriterLaTeX(pymdWriter):
	def pre_code(self, chunk):
		options = [self.syntax_highlight]
		if chunk.options['label'] is not False:
			options.append('#code:%s' % chunk.options['label'])
		if chunk.options['caption'] is not False:
			options.append('caption="%s"' % chunk.options['caption'])
		elif chunk.options['label'] is not False:
			options.append('caption="%s"' % chunk.name)
		options.extend(chunk.pass_options)
		self.wf.write("\n```{%s}\n" % " ".join(options))
		return

	def post_code(self, chunk):
		self.wf.write("```\n\n")
		return

	def pre_error(self, chunk):
		options = ['.alertblock']
		if chunk.options['label'] is not False:
			options.append('#block:%s' % chunk.options['label'])
		if chunk.options['caption'] is not False:
			caption = 'Error at %s' % chunk.options['caption']
		elif chunk.options['label'] is not False:
			caption = 'Error at %s' % chunk.name
		else:
			caption = ''
		options.extend(chunk.pass_options)
		self.wf.write("\n### %s {%s}\n\n" % (caption, ' '.join(options)))
		return

	def post_error(self, chunk):
		self.wf.write("\n<!-- -->\n\n")
		return

	def pre_image(self, chunk, offset):
		self.wf.write("\n")
		return

	def post_image(self, chunk, offset):
		self.wf.write("\n")
		return

	def pre_table(self, chunk):
		pass

	def post_table(self, chunk):
		if chunk.options['label'] is not False:
			if chunk.options['caption'] is not False:
				caption = chunk.options['caption']
			else:
				caption = chunk.name
			caption += " {#tbl:%s}" % chunk.options['label']
			self.wf.write("\n: %s\n\n" % caption)
		elif chunk.options['caption'] is not False:
			self.wf.write("\n: %s\n\n" % chunk.options['caption'])
		else:
			self.wf.write("\n")
		return

	def pre_text(self, chunk):
		options = ['.block']
		if chunk.options['label'] is not False:
			options.append('#block:%s' % chunk.options['label'])
		if chunk.options['caption'] is not False:
			caption = 'Result of %s' % chunk.options['caption']
		elif chunk.options['label'] is not False:
			caption = 'Result of %s' % chunk.name
		else:
			caption = ''
		self.wf.write("\n### %s {%s}\n\n" % (caption, ' '.join(options)))
		return

	def post_text(self, chunk):
		self.wf.write("\n<!-- -->\n\n")
		return


class pymdWriterBeamer(pymdWriterLaTeX):
	def pre_code(self, chunk):
		options = [self.syntax_highlight]
		if chunk.options['label'] is not False:
			options.append('#code:%s' % chunk.options['label'])
		if chunk.options['caption'] is not False:
			options.append('caption="%s"' % chunk.options['caption'])
		elif chunk.options['label'] is not False:
			options.append('caption="%s"' % chunk.name)
		if chunk.options['caption'] is not False:
			title = 'Code of ' + chunk.options['caption']
		else:
			title = 'Code of ' + chunk.name
		options.extend(chunk.pass_options)
		self.wf.write("\n## %s\n" % title)
		self.wf.write("\n```{%s}\n" % " ".join(options))
		return

	def pre_error(self, chunk):
		options = ['.alertblock']
		if chunk.options['label'] is not False:
			options.append('#block:%s' % chunk.options['label'])
		if chunk.options['caption'] is not False:
			caption = 'Error at %s' % chunk.options['caption']
		elif chunk.options['label'] is not False:
			caption = 'Error at %s' % chunk.name
		else:
			caption = ''
		if chunk.options['caption'] is not False:
			title = 'Error at %s' % chunk.options['caption']
		else:
			title = 'Error at %s' % chunk.name
		self.wf.write("\n## %s\n" % title)
		self.wf.write("\n### %s {%s}\n\n" % (caption, ' '.join(options)))
		return

	def pre_image(self, chunk, offset):
		if chunk.options['caption'] is not False:
			title = 'Figure of %s' % chunk.options['caption']
		else:
			title = 'Figure of %s' % chunk.name
		if offset > 0:
			title += "（%d）" % offset
		self.wf.write("\n## %s\n\n" % title)
		return

	def pre_table(self, chunk):
		if chunk.options['caption'] is not False:
			title = 'Table of %s' % chunk.options['caption']
		else:
			title = 'Table of %s' % chunk.name
		self.wf.write("\n## %s\n\n" % title)
		return

	def pre_text(self, chunk):
		if chunk.options['label'] is not False:
			if chunk.options['caption'] is not False:
				caption = 'Result of %s' % chunk.options['caption']
			else:
				caption = 'Result of %s' % chunk.name
			caption += ' {#block:%s}' % chunk.options['label']
		else:
			caption = ''
		if chunk.options['caption'] is not False:
			title = 'Result of %s' % chunk.options['caption']
		else:
			title = 'Result of %s' % chunk.name
		self.wf.write("\n## %s\n" % title)
		self.wf.write("\n### %s\n\n" % caption)
		return


class pymdWriterPython(pymdWriter):
	def write_code(self, chunk):
		self.wf.write("# %s\n" % chunk.name)
		self.wf.write("\n".join(chunk.contents) + "\n")
		return

	def write_document(self, chunk):
		pass


class pymdWriterR(pymdWriter):
	def write_code(self, chunk):
		self.wf.write("# %s\n" % chunk.name)
		self.wf.write("\n".join(chunk.contents) + "\n")
		return

	def write_document(self, chunk):
		pass
