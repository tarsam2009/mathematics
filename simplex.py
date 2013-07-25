from matrix import Matrix
from operator import itemgetter

def simplex_method( matrix, param_count, verbose = False ):
	'''Performs the simplex method given a tableu stored in a matrix'''
	#Keep track of the starting values
	values = range(param_count, matrix.size()[1] - 2)

	#The end condition is inside of the loop
	if verbose:
		print 'Starting'

	while( True ):
		if verbose:
			matrix.display()
		
		column = min(enumerate(matrix.rows[-1][:-1]),
			key=itemgetter(1))[0] 
		
		if matrix.rows[-1][column] >= 0:
			break
		
		if verbose:
			print 'Examining column', column
		
		col_count = matrix.size()[1]
		
		ratios = map( lambda x: (x[1][-1] / x[1][column], x[0]), enumerate(matrix.rows[:-1]) )
		
		value, row = min( filter( lambda x: x[0] > 0, ratios ),
			key=itemgetter(0) )
		
		if verbose:
			print '\tMin {} found at {}'.format( value, row )
		
		value = 1 / float(matrix.rows[row][column])
		matrix.rowMult( value, row )
		
		for i in xrange( matrix.size()[0] ):
			if not i == row:
				matrix.rowMultAdd( -1 * matrix.rows[i][column],
					row, i)
		
		if verbose:
			print values
		values[row] = column
	matrix.display()
	print values
