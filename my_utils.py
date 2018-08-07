class Queue(object):
	"""FIFO Queue, yeah!"""
	_list = []
	def pop(self):
		return _list.pop()

	def push(self, item):
		_list.append(item)

	def isEmpty(self):
		return bool(_list)