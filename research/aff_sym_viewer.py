#!/usr/bin/python

from Tkinter import *
import math

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
	def __init__(self):
		self.coords = [(0,0), (1/math.sqrt(3),1), (-1/math.sqrt(3),1)]
		self.triangle = None

	def action(self, element):
		#Element is 0,1,or 2. We end up flipping the element coord over the other two
		point = self.coords[element]
		axis = list(self.coords)
		axis.pop(element)
		new_point = flip( point, axis[0], sub(axis[0],axis[1]) )
		new_alcove = Alcove()
		new_alcove.coords = list(self.coords)
		new_alcove.coords[element] = new_point
		return new_alcove
	
	def apply_to_canvas(self, canvas, coords, fill=True):
		if self.triangle:
			self.clean(canvas)
		coords[1] = coords[1]*-1
		coords[3] = coords[3]*-1

		scalar = coords[2] - coords[0]
		offset = coords[:2]

		if fill:
			fill='white'
		else:
			fill=''
		
		#First, we need to scale and translate
		coords = map( lambda x: add(scale(x, scalar), offset), self.coords )

		#Next, we need to flip the y values
		coords = map( lambda x: (x[0],x[1]*-1), coords )

		self.triangle = canvas.create_polygon(coords, 
			fill=fill,
			outline='black')
	
	def clean(self, canvas):
		canvas.delete(self.triangle)
	
	def __repr__(self):
		return 'Alcove: {}'.format(self.coords)

class AffineSymmetricViewer( Frame ):
	def __init__(self, actions=None):
		Frame.__init__(self)
		self.actions = actions
		self.alcoves = []
		self.action = 0
		WIDTH,HEIGHT = 300,300
		self.pack(fill=BOTH, expand=1)
		canvas = Canvas(self, width=WIDTH, height=HEIGHT)
		canvas.config(background="gray")
		canvas.pack()
		self.canvas = canvas
		self.last = None
		self.ref = canvas.create_rectangle(0,0,1,1,state=HIDDEN)
		self.canvas.bind('<ButtonRelease-1>', self.release)
		self.canvas.bind('<Button-3>', self.act)
		self.canvas.bind('<B1-Motion>', self.mouse_move)
		self.canvas.bind('<Button-4>', lambda x: self.zoom(0.9,x))
		self.canvas.bind('<Button-5>', lambda x: self.zoom(1.1,x))
		
		self.canvas.scale(ALL, 0, 0, 20, 20)
		self.canvas.move(ALL, WIDTH/2.0, HEIGHT/2.0)

	def zoom( self, scalar, evt ):
		self.canvas.scale(ALL, evt.x, evt.y, scalar, scalar)

	def release( self, evt ):
		self.last=None
	
	def act( self, evt ):
		#If there are actions to act
		if self.actions:
			#Check if any alcoves exist
			new_alcove = None
			if not self.alcoves:
				new_alcove = Alcove()
			elif self.action >= len(self.actions):
				#Reset
				for alcove in self.alcoves:
					alcove.clean(self.canvas)
				self.alcoves = []
				self.action = 0
			else:
				#Do an action
				new_alcove = self.alcoves[-1].action( self.actions[self.action] )
				self.action = self.action+1

			if new_alcove:
				new_alcove.apply_to_canvas( self.canvas, self.canvas.coords(self.ref) )
				self.canvas.itemconfig(new_alcove.triangle, fill='red')
				if self.alcoves:
					self.canvas.itemconfig(self.alcoves[-1].triangle, fill='white')

				self.alcoves.append(new_alcove)
			
	def mouse_move( self, evt ):
		if not self.last:
			self.last = (evt.x,evt.y)

		dx,dy = sub( (evt.x, evt.y), self.last )
		self.last = (evt.x, evt.y)

		self.canvas.move(ALL, dx, dy)

if __name__ == '__main__':
	app = AffineSymmetricViewer([0,2,1,2,2,1,0,1])
	app.mainloop()
