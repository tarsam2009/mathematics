from mathematics import lcm
from operator import itemgetter

def residue_sets(moduli):
	'''Iterator for all possible residue choices given a list of moduli'''
	residues = [0] * len(moduli) #Everything starts at 0
	#Product of the moduli is the number of distinct residue sets
	max_residue_sets = reduce(lambda x,y: x*y, moduli)
	
	for _ in xrange(max_residue_sets):
		yield tuple(residues)
		residues[0] = residues[0] + 1
		
		#Create rollover
		for i in xrange(len(moduli)):
			if residues[i] == moduli[i]:
				residues[i] = 0
				
				if i + 1 != len(moduli):
					residues[i + 1] = residues[i + 1] + 1
			else:
				break

class Congruence:
	'''
	Represents a single residue mod a single modulus
	'''

	def __init__(self, residue = 1, modulus = 1):
		self.residue = residue
		self.modulus = modulus
	
	def contains(self, x):
		'''
		Returns whether 'x' satisfies the congruence
		'''
		return self.residue % self.modulus == x % self.modulus
	
	def filter(self, numbers):
		'''
		Returns which numbers in the list satisfy the congruence
		'''
		return filter(self.contains, numbers)
	
	def coverage(self):
		'''
		Returns what percentage of numbers satisfy this congruence
		'''
		return 1 / float(self.modulus)

	def __lt__(self, other):
		return self.modulus < other.modulus
	
	def __eq__(self, other):
		return self.modulus == other.modulus and self.residue == other.residue

	def __str__(self):
		return '{} (mod {})'.format( self.residue, self.modulus )

	def __repr__(self):
		return self.__str__()

class Covering:
	'''
	Treats a set of congruences as a covering system of the integers
	that can be added to and tested for covering.
	'''
	def __init__(self):
		'''Establishes a covering with no congruences and lcm=1'''
		self.congruences = []
		self.lcm = 1
	
	def add( self, residue, modulus=2 ):
		'''
		Adds the residue/modulus congruence to the congruences and 
		increases the lcm accordingly.
		'''
		if residue.__class__ == Congruence:
			self.congruences.append( residue )
			modulus = residue.modulus
			residue = residue.residue
		else:
			self.congruences.append( Congruence( residue, modulus ) )
		
		if not self.lcm % modulus == 0:
			self.lcm = lcm( self.lcm, modulus )
	
	def fill( self, congruences ):
		'''Adds all the congruences given in the zipped list of residue, modulus tuples'''
		for congruence in congruences:
			self.add( congruence[0], congruence[1] )

	def remove( self, residue, modulus=2 ):
		'''
		Removes the residue/modulus congruence from the congruences
		and decreases the lcm accordingly
		'''
		if residue.__class__ == Congruence:
			self.congruences.remove( residue )
			modulus = residue.modulus
			residue = residue.residue
		else:
			self.congruences.remove( Congruence( residue, modulus ) )

		self.lcm = lcm( filter( lambda x: x.modulus, self.congruences ) )

	def update( self, residue, modulus ):
		'''Replaces the residue for a given modulus'''
		for congruence in self.congruences:
			if congruence.modulus == modulus:
				congruence.residue = residue % modulus
				break

	def __iter__(self):
		'''Iterates through the congruences in order of increasing modulus'''
		
		for congruence in sorted( self.congruences ):
			yield congruence
	
	def __str__(self):
		return ', '.join( map( Congruence.__str__, self.congruences ) )
	
	def __repr__(self):
		return self.__str__()

	def uncovered(self):
		'''Lists the numbers that are not covered by the covering'''
		l = []
		for i in xrange( self.lcm ):
			covered = False

			for congruence in self.congruences:
				if congruence.contains( i ):
					covered = True
					break

			if not covered:
				l.append( i )

		return l
	
	def is_covering( self ):
		'''Checks if all integers up to the lcm are covered'''
		for i in xrange( self.lcm ):
			if not any(map( lambda x: x.contains(i), self.congruences)): 
				return False
	
		return True

	def maximum_coverage( self ):
		'''Returns the sum of the recipricals of the moduli'''
		return sum( map( lambda x: x.coverage(), self ) )		
	
def greedy_covering( moduli, start = 0 ):
	'''
	Returns the best covering produced by greedily selecting moduli.
	'start' dictates which integer is checked first for the covering.
	Moduli are utilized in the order of the 'moduli' iterable
	'''
	lcm_of_moduli = lcm( moduli )
	uncovered = range( lcm_of_moduli )
	covering = Covering()
	
	#For each modulus
	for modulus in moduli:
		best_residue = 0
		best_count   = 0
		
		congruence = Congruence( start%modulus, modulus )

		#Look at all possible residues
		for residue in xrange( start, start + lcm_of_moduli ):
			congruence.residue = residue % modulus
			count = len( congruence.filter( uncovered ) )
		
			#check if this is the best residue so far
			if count > best_count:
				best_residue = residue
				best_count = count
		
		#Add best congruence to the system
		covering.add( best_residue, modulus )
		
		#Update which integers need to be covered
		congruence.residue = best_residue % modulus
		uncovered = list( set(uncovered) - set(congruence.filter( uncovered )))
	return covering
