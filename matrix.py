import exceptions

class MatrixError(ArithmeticError):
	pass

class Matrix:
	def __init__(self):
		self.rows = []
	
	def size(self):
		rows = len( self.rows )
		
		if rows > 0:
			return rows, len(self.rows[0])
		else:
			return 0,0
	
	def rowMult( self, val, a ):
		newRow = map( lambda x: val*x, self.rows[a] )
		self.rows[a] = newRow

	def rowMultAdd( self, val, a, b ):
		newRow = map( lambda x: val * x, self.rows[a] )
		newRow = map( lambda x: x[0] + x[1], zip( self.rows[b], newRow ) )
		self.rows[b] = newRow
	
	def display(self):
		for row in self.rows:
			print ' '.join( map( str, row) )
	
	def row(self, i):
		m = Matrix()
		m.rows.append(self.rows[i])
		return m
	
	def col(self, i):
		m = Matrix()
		for row in self.rows:
			m.rows.append( [ row[i] ] )
		return m
	
	def add(self, o):
		if self.size() != o.size():
			raise MatrixError('Dimensions {} and {}'.format(self.size(), o.size()))
		
		rows, cols = self.size()
		m = Matrix()
		m.rows = [ [0] * cols ] * rows
		
		for i in xrange(rows):
			for j in xrange(cols):
				m.rows[i][j] = self.rows[i][j] + o.rows[i][j]
		
		return m
