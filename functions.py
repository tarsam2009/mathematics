class Polynomial:
	def __init__( self, coeff = 1):	
		if coeff.__class__ == list:
			self.coefficients = coeff
		elif coeff.__class__ == int:
			self.coefficients = [0] * coeff
		else:
			self.coefficients = [0]
	
	def at( self, x ):
		return reduce(lambda a,b:a+b, map(lambda a: a[1]*(x**a[0]), enumerate(self.coefficients)))
	
	def __str__( self ):
		return ' + '.join( map( lambda x: '{0}x^{1}'.format(x[1],x[0]), enumerate(self.coefficients) ) )

	
def discreteDerivative( numbers ):
	derivative = []
	for i in xrange( len(numbers) - 1 ):
		derivative.append( numbers[i+1] - numbers[i] )
	return derivative


