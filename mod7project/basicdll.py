# basicdll.py:
# This is a rudimentary dll implementation, with some details still missing.

class DLLitem():
	def __init__(self, value, prev):
		"""
		Creates a new DLL item, with value <value>.
		It is inserted in the DLL after <prev>, which is either another DLL item,
		or the DLL itself (then this will be the first item).
		"""
		self.val = value
		nxt = prev.nxt
		self.prev = prev
		self.nxt = nxt
		nxt.prev = self
		prev.nxt = self
		
	def __repr__(self):
		return 'DLLitem(' + repr(self.val) + ')'

	def delete(self):
		self.prev.nxt, self.nxt.prev = self.nxt, self.prev
		
class DLL():
	def __init__(self, initlist=[]):
		self.prev = self
		self.nxt = self
		for val in initlist:
			self.append(val)
		
	def __repr__(self):
		if self.nxt == self:
			return 'DLL()'
		s = 'DLL(['
		obj = self.nxt
		while obj != self:
			s += repr(obj.val) + ','
			obj = obj.nxt
		s = s[:-1] + '])'
		return s
		
	def append(self, newvalue):
		return DLLitem(newvalue, self.prev)
		
	def isempty(self):
		"""
		Returns True iff the DLL is empty.
		"""	
		if self.nxt == self:
			return True
		else:
			return False
	

	# From here: fill in the details yourself, after implementing the 
	# DLLitem's delete method:

	def insert(self, newvalue):
		return DLLitem(newvalue, self)
	
	
	def pop(self):
		last = self.prev.val
		self.prev.delete()
		return last
		
	def dequeue(self):
		first = self.nxt.val
		self.nxt.delete()
		return first
	
	def __getitem__(self, i):
		step = -1 if i>=0 else 1
		done = False
		result = self
		while not done:
			if step == -1:
				result = result.nxt
			else:
				result = result.prev
			if result == self:
				raise IndexError
			done = i == 0 or i == -1
			i += step
		return result.val
	
	def __setitem__(self, i, val):
		step = -1 if i>=0 else 1
		done = False
		result = self
		while not done:
			if step == -1:
				result = result.nxt
			else:
				result = result.prev
			if result == self:
				raise IndexError
			done = i == 0 or i == -1
			i += step
		result.val = val
		
	