import math
from mathematics.research.lattice import hikita_from_word

def project( old_vector, projecting ):
	return scale(projecting, dot(old_vector, projecting) / dot( projecting, projecting ))

def dot( v1, v2 ):
	return float(sum( map( lambda x: x[0]*x[1], zip(v1,v2) ) ))

def scale( v, s ):
	return tuple( map( lambda x: x*s, v ) )

def normal( v ):
	return v[1], -v[0]

def add( u, v ):
	return tuple( map( lambda x: x[0] + x[1], zip(u,v) ) )

def sub( u, v ):
	return add( u, scale(v,-1))

def flip( point, line_base, line_vec ):
	n = normal(line_vec)
	v = sub(point, line_base)
	p = project( v, n )
	return add( point, scale(p,-2) )

class Alcove:
	def __init__(self, copy=None):
		if copy:
			self.coords = copy.coords
		else:
			self.coords = [(0,0), (1/math.sqrt(3),1), (-1/math.sqrt(3),1)]
		
		self.triangle = None

	@staticmethod
	def init_from_word( actions ):
		alcove = Alcove()
		for action in actions:
			alcove = alcove.action( action )

		return alcove

	def action(self, element):
		if element > 2:
			raise ArithmeticError('Can only act on an alcove with 0,1, or 2')
		#Element is 0,1,or 2. We end up flipping the element coord over the other two
		point = self.coords[element]
		axis = list(self.coords)
		axis.pop(element)
		new_point = flip( point, axis[0], sub(axis[0],axis[1]) )
		new_alcove = Alcove()
		new_alcove.coords = list(self.coords)
		new_alcove.coords[element] = new_point
		return new_alcove
	
	def apply_to_canvas(self, canvas, coords):
		if self.triangle:
			self.clean(canvas)
		coords[1] = coords[1]*-1
		coords[3] = coords[3]*-1

		scalar = coords[2] - coords[0]
		offset = coords[:2]

		center = self.coords[0]

		#Make the hexagon
		hexagon = []
		for vec in [(-1/math.sqrt(3),1), (1/math.sqrt(3),1), (1.1547,0), (1/math.sqrt(3),-1), (-1/math.sqrt(3),-1), (-1.1547,0) ]:
			hexagon.append( add(center,vec) )

		#First, we need to scale and translate
		tri_coords = map( lambda x: add(scale(x, scalar), offset), self.coords )
		hexagon = map( lambda x: add(scale(x, scalar), offset), hexagon)


		#Next, we need to flip the y values
		tri_coords = map( lambda x: (x[0],x[1]*-1), tri_coords )
		hexagon = map( lambda x: (x[0],x[1]*-1), hexagon )

		#Then make some shapes
		self.triangle = canvas.create_polygon(tri_coords, 
			outline='black')

		self.hex = canvas.create_polygon(hexagon, fill='', outline='black')

		for i in range(3):
			canvas.create_line( [ hexagon[i], hexagon[(i+3)%6] ] )

		radius = 0.15 * scalar

		center = tri_coords[0]

		bbox = sub( center, (radius,radius) ) + add( center, (radius,radius) )
		self.circle = canvas.create_oval(bbox, fill='black')
	
	def clean(self, canvas):
		canvas.delete(self.triangle)
		canvas.delete(self.circle)
	
	def get_planar_point(self):
		m = int(round(dot( ( 1.0/2.0/math.sqrt(3), 0.5), self.coords[0] )))
		n = int(round(dot( (-1.0/2.0/math.sqrt(3), 0.5), self.coords[0] )))

		return add(scale( (1,-1,0), m ), scale( (0,1,-1), n ))

	def __repr__(self):
		return 'Alcove: {}'.format(self.coords)

def all_reduced_words( start, n=3 ):
	unexpanded = [list(start)]
	expanded = list()

	while unexpanded:
		seed = unexpanded.pop()
		expanded.append( seed )

		for i in range(len(seed)-2):
			neighbors = ((seed[i]+1)%n == seed[i+1]) or ((seed[i+1]+1)%n == seed[i])

			if seed[i] == seed[i+2] and neighbors:
				newseed = list( seed )
				newseed[i:i+3] = [seed[i+1], seed[i], seed[i+1]]
				if newseed not in expanded:
					unexpanded.append(newseed)
	
	return expanded
	
#Compare two affine words. If a <= b, return true. Else false. (so they may not even be compareable)
def affine_less_than( a, b ):
	if len(a) == 0: return True
	if len(b) == 0: return False

	words_of_a = [ ','.join(map(str,x)) for x in all_reduced_words(a)]

	for word in all_reduced_words( b ):
		#Check if word contains some word of a
		word = ','.join(map(str,word))

		#print 'Checking',[word]

		for aword in words_of_a:
			#print '\tAgainst', aword
			if aword in word:
				break
		else: #No word found
			#print 'No {} found in {}'.format( word, words_of_a )
			return False
	
	return True


