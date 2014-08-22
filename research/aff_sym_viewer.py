#!/usr/bin/python

from Tkinter import *
from mathematics.research.affine_sym import *
import thread
import time

class AffineSymmetricViewer():
	def __init__(self, actions, animate=False, complete=True):
		self.window = Tk()
		self.window.title(str(actions))
		self.actions = actions
		self.alcoves = []
		self.action = 0
		WIDTH,HEIGHT = 300,300
		#self.window.pack()
		canvas = Canvas(self.window, width=WIDTH, height=HEIGHT)
		canvas.config(background="gray")
		canvas.pack()
		self.canvas = canvas
		self.last = None
		self.ref = canvas.create_rectangle(0,0,1,1,state=HIDDEN)
		self.canvas.bind('<ButtonRelease-1>', self.release)
		self.canvas.bind('<Button-3>', self.mouse)
		self.canvas.bind('<B1-Motion>', self.mouse_move)
		self.canvas.bind('<Button-4>', lambda x: self.zoom(0.9,x))
		self.canvas.bind('<Button-5>', lambda x: self.zoom(1.1,x))
		
		self.canvas.scale(ALL, 0, 0, 20, 20)
		self.canvas.move(ALL, WIDTH/2.0, HEIGHT/2.0)

		if complete:
			#Fast forward
			for _ in range(len(self.actions)+2):
				self.act()

		if animate:
			#Start a thread, which is stopped by right click
			self.running = True
			def animation(self):
				while self.running:
					time.sleep(1)
					self.act()
			
			self.thread = thread.start_new_thread( animation, (self,) )
		else:
			self.thread = None

		def close():
			self.running=False
			self.window.destroy()

		self.window.protocol("WM_DELETE_WINDOW",close)
		self.window.mainloop()

	def zoom( self, scalar, evt ):
		self.canvas.scale(ALL, evt.x, evt.y, scalar, scalar)

	def release( self, evt ):
		self.last=None
	
	def act( self ):
		#If there are actions to act
		if self.actions:
			#Check if any alcoves exist
			new_alcove = None
			if not self.alcoves:
				new_alcove = Alcove()
			elif self.action == len(self.actions):
				self.canvas.itemconfig(self.alcoves[-1].triangle, fill='green')
				self.action = self.action+1
			elif self.action > len(self.actions):
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

				#Identify the origin
				if self.alcoves:
					self.canvas.itemconfig(self.alcoves[0].triangle, fill='blue')
				self.alcoves.append(new_alcove)

	def mouse( self, evt ):
		if self.thread:
			self.keep_running = False
		else:
			self.act()
	
	def mouse_move( self, evt ):
		if not self.last:
			self.last = (evt.x,evt.y)

		dx,dy = sub( (evt.x, evt.y), self.last )
		self.last = (evt.x, evt.y)

		self.canvas.move(ALL, dx, dy)
