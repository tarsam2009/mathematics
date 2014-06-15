class Partition:
	'''This is a partition'''

	def __init__( self, previous=None ):
		'''Create a partition from an iterable which is decreasing'''
		self.parts = []

		#Remove zeros
		if previous:
			self.parts = list( previous )
			if len( self.parts ) > 0:
				#Verify parts are decreasing
				for i in range( len( self.parts ) - 1 ):
					if self.parts[i] < self.parts[i+1]:
						raise ArithmeticError( 'Partition must be weakly decreasing' )

		#Trim any zeros
		while self.parts and self.parts[-1] == 0:
			self.parts.pop()
	
	@staticmethod
	def affine_to_core( reduced_word = None, n = 1 ):
		'''Create a n-core generated from the reduced word for an affine grassmannian element'''
		if not reduced_word: reduced_word = []

		p = Partition()
		while reduced_word:
			p = p.core_affine_action( reduced_word.pop(), n )

		return p
	
	@staticmethod
	def affine_to_bounded( reduced_word = None, n = 1 ):
		'''Created a bounded partition in bijection with the reduced word'''
		return Partition.affine_to_core( reduced_word, n ).core_to_bounded(n)
	
	def bounded_to_core( self, n ):
		p = Partition( self )
		
		#Make starting cells
		starts = [1] * len(p)

		for row in reversed(range(1,len(p)+1)):
			#print('Checking row {0}'.format(row))

			while any( map(lambda x: x.hook_length(p) >= n+1, CellIterator( p, row, (row,starts[row-1]) ) ) ):
				#print('\tCell ({0},{1}) fails {2}'.format(row,starts[row-1],p))
				for r in range(row):
					p.parts[r] = p.parts[r] + 1
					starts[r] = starts[r] + 1
				#print('\t\tShifted to {0}'.format( p ) )
			#	#shift the cells

		#For each row, check if any hook lengths too big (n+1)
		return p
	
	def core_affine_action( self, element, n ):
		#Go through the addable blocks
		removable = []
		addable = []
		for i in range(len(self)):
			new_parts = list(self)
			try:
				new_parts[i] = self[i]+1
				Partition(new_parts)
				addable.append( i )
			except ArithmeticError:
				pass

			new_parts = list(self)
			try:
				new_parts[i] = self[i]-1
				Partition(new_parts)
				removable.append( i )
			except ArithmeticError:
				pass

		addable = filter( lambda x : PartitionCell(x+1,self.parts[x]+1).content( n ) == element, addable)
		if (-1 * len(self)) % n == element:
			addable.append( len(self) )
		removable = filter( lambda x : PartitionCell(x+1,self.parts[x]).content( n ) == element, removable )

		new_parts = list(self)
		new_parts.append(0)

		for r in addable:
			new_parts[r] = new_parts[r] + 1
		for r in removable:
			new_parts[r] = new_parts[r] - 1
			
		return Partition(new_parts)
	
	def core_to_bounded( self, n ):
		p = Partition( self )
		
		for row in range(1,len(p)+1):
			p.parts[row-1] = len( [x for x in CellIterator(self, row) if x.hook_length(self) <= n] )

		return p
	
	def bounded_to_affine( self, n ):
		return map(lambda x: x.content(n), reversed(list(self.cells)))

	@property
	def size( self ):
		'''Return the total number of cells in the partition'''
		if len( self ) == 0:
			return self
		else:
			return sum( self.parts )
	
	@property
	def cells( self ):
		return CellIterator( self )
	
	def row_cells( self, row ):
		return CellIterator( self, row )

	# Override common builtin methods
	def __repr__( self ):
		return 'Partition' + str( self.parts )

	def __iter__( self ):
		return self.parts.__iter__()
	
	def __len__( self ):
		return len( self.parts )
	
	def __getitem__( self, index ):
		return self.parts[index]
	
class CellIterator:
	def __init__( self, partition, row=None, start=None ):
		self.partition = Partition( partition )

		if not start:
			if row:
				self.cell = PartitionCell( row,1 )
			else:
				self.cell = PartitionCell( 1, 1 )

		else:
			self.cell = PartitionCell( start[0], start[1] )

		self.cell_count = 0
		self.row = row
	
	def __iter__( self ):
		return self

	def next( self ):
		#print('Checking cell ' + str(self.cell.coord))
		#If this is empty, there is nothing to worry about
		if self.partition.size == 0:
			#print('Partition too small')
			raise StopIteration

		if not self.cell.contained_in( self.partition ) or (self.row and (not self.row == self.cell.row)):
			#print('{0} not contained in {1}'.format( self.cell, self.partition ))
			raise StopIteration
		
		return_val = self.cell

		#Increment it
		row, col = self.cell.coord
		#print('\tRow {0}, Col{1}'.format(row,col))
		col = col+1
		if col > self.partition[row-1]:
			row, col = row + 1, 1

		self.cell = PartitionCell( row, col )
		return return_val
	
class PartitionCell:
	'''This is a cell of a partition'''

	def __init__( self, row=1, col=1):
		self.coord = (row, col)
		self.row = row
		self.col = col
	
	def __repr__( self ):
		return 'PartitionCell{0}'.format( self.coord )
	
	def hook_length( self, partition ):
		if not self.contained_in( partition ):
			raise ArithmeticError('Hook length not applicable to {0} in {1}'.format(cell.coord, partition))

		row, col = self.coord

		#Measure how much extra to the right
		length = partition[self.row - 1] - self.col
		
		r = self.row

		while r <= len(partition) and partition[r-1] >= self.col:
			r = r + 1
			length = length + 1
			
		return length
	
	def contained_in( self, partition ):
		row,col = self.coord
		return len( partition ) >= row and partition[row-1] >= col
	
	def content( self, modulus ):
		row, col = self.coord
		return (col - row) % modulus

#def affine_to_hikita( reduced_word = [], n = 1 ):
	
