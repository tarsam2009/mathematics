def gcd(a, b=None):
	"""Return greatest common divisor using Euclid's Algorithm."""
	if( b ): #If we have two numbers
		while b:      
			a, b = b, a % b
		return a
	else: #Otherwise, we should have gotten an iterable
		return reduce(gcd, a)

def lcm(a, b=None):
	"""Return lowest common multiple."""
	if( b ): #If we have two numbers
		return a * b / gcd(a, b)
	else: #It should be an iterable
		return reduce( lcm, a )

def fact(n):
	if n <= 1:
		return 1
	ans = long( 1 )
	return reduce( lambda x,y: x*y, xrange(1,n+1) )

def comb(n,r):
	if r > n:
		return 0
	
	n = long(n)
	r = long(r)
	return fact( n ) /  ((fact(n-r) * fact(r)))
