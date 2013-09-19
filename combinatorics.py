def factorial( n ):
	if n <= 1:
		return 1
	ans = long( 1 )
	return reduce( lambda x,y: x*y, xrange(1,n+1) )

def combinations( n, k ):
	if k > n:
		return 0
	
	n, k = long(n), long(k)

	return factorial( n ) / ( factorial(n-k) * factorial(k) )


class BinomialCoefficient:
	def __init__( self, n = 1, k = 0 ):
		self.n = n;
		self.k = k;
	
	def eval( self ):
		return combinations( self.n, self.k )
	
	def __str__( self ):
		return '{0}C{1}'.format(self.n, self.k)
	
	def __repr__( self ):
		return self.__str__()

#Do the functional conversions

def discrete_derivative( values ):
	result = []
	for i in xrange( len( values ) - 1 ):
		result.append( values[i+1] - values[i] )
	
	return result

def convert_to_binomial_coefficients( f, degree=20 ):
	derivatives = []
	derivatives.append( map( f, xrange(degree) ) )

	print derivatives[0]

	for i in xrange( degree - 1 ):
		derivatives.append( discrete_derivative( derivatives[i] ) )
		print derivatives[i + 1]
	
	if derivatives[0][0] != 0:
		#print 'Failed to find {0} degree polynomial'.format( degree )
		return None
	else:
		first_zeros = degree
		for i in reversed( xrange(1, degree - 1) ):
			if any( map( lambda x: not x==0, derivatives[i] ) ):
				first_zeros = i + 1
				break
		
		return map(lambda x: x[0], derivatives)[:first_zeros]
