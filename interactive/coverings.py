import pyglet
from pyglet.gl import *
from mathematics import lcm
from time import sleep

class InteractiveCovering:
	def __init__( self, moduli, lcm, residues = None ):
		self.moduli = moduli
		if not residues:
			residues = [0] * len(moduli)
		self.residues = residues
		self.lcm = lcm
		self.row = 0
		window = pyglet.window.Window(resizable=True)
		window.push_handlers( self.on_draw, self.on_resize, self.on_key_press )
		pyglet.app.run()
	
	def on_resize( self, w, h ):
		self.width = w
		self.height = h
		glViewport(0, 0, w, h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, w, 0, h, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		return pyglet.event.EVENT_HANDLED
	
	def on_key_press( self, symbol, modifiers ):
		if symbol == pyglet.window.key.UP:
			self.row = (self.row + 1) % len( self.moduli )
		if symbol == pyglet.window.key.DOWN:
			self.row = (self.row - 1) % len( self.moduli )
		if symbol == pyglet.window.key.LEFT:
			self.residues[self.row] = (self.residues[self.row] - 1) % self.moduli[self.row]
		if symbol == pyglet.window.key.RIGHT:
			self.residues[self.row] = (self.residues[self.row] + 1) % self.moduli[self.row]

	def on_draw( self ):
		glClearColor(1.0,1.0,1.0,0.0)
		glClear( GL_COLOR_BUFFER_BIT )
		
		square_length = self.width / self.lcm
		
		glBegin( GL_QUADS )
		
		#Draw the current row background
		glColor3f(0,0,0.2)
		y = self.row * square_length
		glVertex2f( 0, y )
		glVertex2f( self.width, y )
		glVertex2f( self.width, y + square_length )
		glVertex2f( 0, y + square_length )
		
		glColor3f(1,0,0)
		
		#Draw the residue patterns
		rowCounts = [0] * self.lcm
		y = 0
		for residue, modulus in zip(self.residues, self.moduli):
			#print '{} (mod {})'.format(residue, modulus)
			#sleep(3)
			for x in xrange(residue, self.lcm, modulus):
				rowCounts[x] = rowCounts[x] + 1
				x = x * square_length
				
				glVertex2f( x, y )
				glVertex2f( x + square_length, y )
				glVertex2f( x + square_length, y + square_length )
				glVertex2f( x, y + square_length )
				
			y = y + square_length
		
		#Draw the row counts
		m = len( self.moduli )
		y = m * square_length
		x = 0
		
		for count in rowCounts:
			color = float(m - count) / len( self.moduli )
			
			glColor3f(color,color,color)
			
			glVertex2f( x, y )
			glVertex2f( x + square_length, y )
			glVertex2f( x + square_length, y + square_length )
			glVertex2f( x, y + square_length )
			x = x + square_length
		
		glEnd()
