'''Methods for converting between the coroot lattice of the
affine symmetric group and the Hikita tuples'''

def lattice_to_hikita( point ):
	point = list(point)

	if sum( point ) != 0:
		raise ArithmeticError('Lattice coordinate {0} does not sum to zero'.format(point))
	
	n = len( point )
	result = [0] * (n-1)

	#Zero maps to zero
	if all( map( lambda x: x==0, point ) ):
		return result
	
	#First, find the largest index of the smallest value
	min_val = min( point )
	functional_k = max( filter(lambda x: x[1]==min_val, enumerate(point) ), key=lambda x: x[0] )[0]
	actual_k = functional_k+1

	m = -min_val-1
	
	#print 'm,k=',m,actual_k

	#Remove the k-th component
	point.pop(functional_k)
	
	#print point

	#Add m to everything
	incremented = map( lambda x: x+m, point )
	
	#print incremented
	#Wrap the tuple around and increment the second part
	result = incremented[functional_k:] + map( lambda x: x+1, incremented[:functional_k] ) 
	return tuple(result)

def hikita_action( point, action, n=3 ):
	point = list(point)

	if action >= n:
		raise ArithmeticError( 'Action not bounded by n' )
	
	a = sum( point )
	l = (action - a) % n
	#print 'l', l

	if l == 0:
		i = point.pop(0)
		point.append(i+1)
	elif l < n-1:
		point[l-1], point[l] = point[l], point[l-1]
	else: #l == n-1
		if point[-1] == 0:
			pass #Do nothing
		else:
			i = point.pop(-1)
			point.insert(0, i-1)
	
	return tuple(point)

def hikita_to_lattice( point ):
	point = list(point)

	#Verify they are positive
	if any( map( lambda x: x<0, point ) ):
		raise ArithmeticError('Hikita point {0} is not a positive tuple'.format( point ))

	n = len(point) + 1

	if sum( point ) == 0:
		return tuple([0] * n)

	#By def of k, so n = length + 1
	m,actual_k = divmod( sum( point ), n )

	#However, by def of k, it must be >= 0
	if actual_k == 0:
		actual_k = n
		m = m - 1

	#print 'm,k=',m, actual_k
	functional_k = actual_k - 1

	result = list(point)

	#decrease everything by m
	result = map( lambda a: a-m, result )

	#Rearrange everything, n-k+1, n-k+2, ... , n-1, (k-th pos ), 1, 2, ... , n-k
	result = map( lambda a: a-1, result[n-actual_k:] ) + [-m-1] + result[:n-actual_k]

	return tuple(result)
