#!/usr/bin/python
def project( old_vector, projecting ):
	return scale(projecting, dot(old_vector, projecting) / dot( projecting, projecting ))

def dot( v1, v2 ):
	return float((v1[0] * v2[0]) + (v1[1] * v2[1]))

def scale( v, s ):
	return tuple( map( lambda x: x*s, v ) )

def normal( v ):
	return v[1], -v[0]

def add( u, v ):
	return u[0]+v[0],u[1]+v[1]

def sub( u, v ):
	return add( u, scale(v,-1))

def flip( point, line_base, line_vec ):
	n = normal(line_vec)
	v = sub(point, line_base)
	p = project( v, n )
	return add( point, scale(p,-2) )

if __name__ == '__main__':
	v = (1,0)
	print scale(v, 2)
	print dot(v, (3,1))
	print flip( (0,1), (1,0), (1,0) )

