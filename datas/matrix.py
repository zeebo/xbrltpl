class Matrix(object):
	"""Creates a 2d matrix that has operations to remove rows
		columns and grow/shrink without having to worry about it

		Deprecated because of tree based facts"""
	
	def __init__(self, default=None):
		self._data = [[]]
		self.default = default
	
	def _check_index(self, index):
		if index[0] < 0 or index[1] < 0:
			raise IndexError('Must be non-negative indicies')
		
		if len(index) > 2:
			raise IndexError('Indicies must be two dimensional')
		
	
	def __getitem__(self, index):
		self._check_index(index)
		row, col = index
		try:
			return self._data[row][col]
		except IndexError:
			return self.default
	
	def __setitem__(self, index, data):
		self._check_index(index)
		row, col = index
		try:
			self._data[row][col] = data
		except IndexError:
			self._assert_rows(row)
			self._assert_cols(col, row=row)
			self[row, col] = data
	
	def __delitem__(self, index):
		self._check_index(index)
		self[index] = self.default

	def _assert_rows(self, row):
		if len(self._data) <= row:
			rows_to_add = row - len(self._data) + 1
			for _ in xrange(rows_to_add):
				self._data.append([])
	
	def _assert_cols(self, col, row=0):
		self._assert_rows(row)
		column = self._data[row]
		if len(column) <= col:
			cols_to_add = col - len(column) + 1
			for _ in xrange(cols_to_add):
				column.append(self.default)