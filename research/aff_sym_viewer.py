#!/usr/bin/python

from Tkinter import *
from mathematics.research.affine_sym import *
import thread
import time

colors = ['white','blue','green','red','orange','purple','black','yellow','cyan','magenta']
class AffineSymmetricViewer():
	def __init__(self, words ):
		self.window = Tk()
		self.window.title('{} Affine Symmetric Words'.format(len(words)))
		WIDTH,HEIGHT = 300,300
		canvas = Canvas(self.window, width=WIDTH, height=HEIGHT)
		canvas.config(background="gray")
		canvas.pack( side=TOP, fill=BOTH, expand=1)
		self.canvas = canvas
		self.ref = canvas.create_rectangle(0,0,1,1,state=HIDDEN)
		self.canvas.bind('<ButtonRelease-1>', self.release)
		self.canvas.bind('<B1-Motion>', self.mouse_move)
		self.canvas.bind('<Button-4>', lambda x: self.zoom(0.9,x))
		self.canvas.bind('<Button-5>', lambda x: self.zoom(1.1,x))
		
		self.canvas.scale(ALL, 0, 0, 20, 20)
		self.canvas.move(ALL, WIDTH/2.0, HEIGHT/2.0)

		self.add_words( words )

		#Make the mouse work
		self.last = None

		self.window.mainloop()

	def add_words( self, words ):
		
		for word in words:
			#Make the alcove
			alcove = Alcove.init_from_word( word )
			h_weight = sum( hikita_from_word( word ) )
			alcove.apply_to_canvas( self.canvas, self.canvas.coords(self.ref))
			self.canvas.itemconfig(alcove.triangle, fill=colors[h_weight%len(colors)])
	
	def release( self, evt ):
		self.last = None

	def zoom( self, scalar, evt ):
		self.canvas.scale(ALL, evt.x, evt.y, scalar, scalar)
	
	def mouse_move( self, evt ):
		if not self.last:
			self.last = (evt.x,evt.y)

		dx,dy = sub( (evt.x, evt.y), self.last )
		self.last = (evt.x, evt.y)

		self.canvas.move(ALL, dx, dy)
