#!/usr/bin/env python3
# -+- coding:utf-8 -*-

import os
from queue import Empty
from jupyter_client.manager import start_new_kernel


def get_pymdProcessor(ptype, kernel):
	if ptype == 'jupyter':
		return pymdProcessorJupyter(kernel)
	elif ptype == '':
		return pymdProcessor(kernel)
	else:
		raise Exception("Incorrect processor type")


class pymdProcessor(object):
	def __init__(self, kernel):
		self.name = kernel
		self.timeout = -1
		return

	def start_kernel(self):
		pass

	def stop_kernel(self):
		pass

	def run_cell(self, chunk):
		pass

	def run(self, contents):
		self.start_kernel()
		for chunk in contents:
			if chunk.chunk_type != 'code':
				continue
			if chunk.options['evaluate'] is False:
				continue
			self.run_cell(chunk)
		self.stop_kernel()
		return


class pymdProcessorJupyter(pymdProcessor):
	def start_kernel(self):
		self.is_ready = False
		self.execute_status = ''
		try:
			self.manager, self.client = start_new_kernel(
				kernel_name=self.name,
				stderr=open(os.devnull, 'w')
			)
		except RuntimeError:
			raise
		self.client.allow_stdin = False
		self.session_id = self.client.session.session
		self.is_ready = True

	def stop_kernel(self):
		self.execute_status = ''
		self.is_ready = False
		self.client.stop_channels()
		self.manager.shutdown_kernel(now=True)

	def is_from_here(self, msg_id, msg):
		parent = msg['parent_header']
		from_here = parent.get("session", self.session_id) == self.session_id
		from_this = parent.get("msg_id") == msg_id
		return from_here and from_this

	def handle_iopub(self, msg_id, chunk):
		timeout = self.timeout if self.timeout > 0 else None
		while self.client.iopub_channel.msg_ready():
			try:
				msg = self.client.get_iopub_msg(timeout=timeout)
			except Empty:
				raise
			msg_type = msg['header']['msg_type']
			if self.is_from_here(msg_id, msg):
				if msg_type == 'status':
					self.execute_status = msg['content']["execution_state"]
					return
				elif msg_type == 'stream':
					if msg['content']["name"] == "stdout":
						chunk.results.append({"text/plain": msg["content"]["text"]})
					elif msg['content']['text'] == "stderr":
						chunk.error = msg["content"]["text"]
				elif msg_type == 'execute_result':
					chunk.results.append(msg["content"]["data"])
					if "image/png" in msg["content"]["data"]:
						chunk.num_image += 1
						msg["content"]["data"]["image_offset"] = chunk.num_image
				elif msg_type == 'display_data':
					chunk.results.append(msg["content"]["data"])
					if "image/png" in msg["content"]["data"]:
						chunk.num_image += 1
						msg["content"]["data"]["image_offset"] = chunk.num_image
				elif msg_type == 'execute_input':
					pass
				elif msg_type == 'error':
					self.is_ready = False
					chunk.error = "\n".join(msg["content"]["traceback"])
					return

	def run_cell(self, chunk):
		if not self.is_ready:
			return
		if len(chunk.contents) < 1:
			return
		print("run chunk %d" % chunk.offset)
		src = "\n".join(chunk.contents)
		while self.client.shell_channel.msg_ready():
			self.client.shell_channel.get_msg()
		msg_id = self.client.execute(src)
		self.execute_status = 'busy'
		while self.execute_status != 'idle' and self.client.is_alive():
			self.handle_iopub(msg_id, chunk)
