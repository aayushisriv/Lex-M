"""


Date:18-04-2020

@author- Aayushi Srivastava
This code performs LEx-M as mentioned in the paper of Pinar Heggernes: Minimal Triangulations of graphs: A survey
"""



import Tkinter
import tkMessageBox
import random
import networkx as nx 
import copy

import LexM as LM 

def isStrInt(str):
	"""function to check if str is int or not"""
	try: 
		int(str)
		return True
	except ValueError:
		return False

class gui_tk(Tkinter.Tk):
	"""The main class contains gui_tk initialization"""

	def __init__(self,parent):
		"""function to initialize the instance of Tkinter and ChordalGraph"""
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()
		self.cg = LM.LexM(0,0)
		self.G = False
		#self.H = False
		# self.Ncg = {}

	def initialize(self):
		"""function to initialize the components in the gui"""
		self.grid()
		#Start of First label
		self.lblNumNodesText = Tkinter.StringVar()
		lblNodes = Tkinter.Label(self, textvariable=self.lblNumNodesText)
		lblNodes.grid(row=0, column=0, sticky=Tkinter.W)
		self.lblNumNodesText.set(u'Number of Nodes')

		self.nodesEntry = Tkinter.Entry(self)
		self.nodesEntry.grid (row=0, column=1, sticky=Tkinter.W)

		#End of first label

		#Start of Second Label

		self.lblNumEdgesText = Tkinter.StringVar()
		lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
		lblEdges.grid(row=1, column=0, sticky=Tkinter.W)
		self.lblNumEdgesText.set(u'No. of Edges ')
	
		self.edgesEntry = Tkinter.Entry(self)
		self.edgesEntry.grid (row=1, column=1, sticky=Tkinter.W)

		#End of second label

		#four buttons
		#Create arbitrary graph
		buttonCreateCG = Tkinter.Button(self,text=u'Generate Arbitrary Graph', 
										   command=self.onCreateCGClick)
		buttonCreateCG.grid(row=2, column=0, sticky=Tkinter.W)
		
		#view arbitrary graph
		buttonViewCG = Tkinter.Button(self,text=u'View Arbitrary Graph', 
										   command=self.onViewCGClick)
		buttonViewCG.grid(row=2, column=1, sticky=Tkinter.W)        
		
		#Create chordal graph
		buttonCreateNCG = Tkinter.Button(self,text=u'Generate Chordal Graph', 
											  command=self.onCreateNCGClick)
		buttonCreateNCG.grid(row=3, column=0, sticky=Tkinter.W)
		
		#View  chordal graph
		buttonViewWCG = Tkinter.Button(self,text=u'View Chordal Graph', 
											 command=self.onViewNCGClick)
		buttonViewWCG.grid(row=3, column=1, sticky=Tkinter.W)

		#View Display of final written results
		buttonCreateNCG = Tkinter.Button(self,text=u'Generate Chordal Graph', 
											  command=self.onCreateNCGClick)
		buttonCreateNCG.grid(row=3, column=0, sticky=Tkinter.W)
		
		#View  chordal graph
		buttonViewWCG = Tkinter.Button(self,text=u'Display Final Results', 
											 command=self.onDisplayResultClick)
		buttonViewWCG.grid(row=4, column=0, sticky=Tkinter.W)

	def onCreateCGClick(self):
		"""function to check valid input and to create arbitrary Graph"""

		noNodes = self.nodesEntry.get()
		if isStrInt(noNodes):
			noNodes = int (self.nodesEntry.get())
			if (noNodes < 4):
				tkMessageBox.showwarning("Warning","Entry for nodes is less than 4.")
				return
		else:
			tkMessageBox.showwarning("Warning","Entry for nodes is not an integer.")
			return

		noEdges = self.edgesEntry.get()
		if isStrInt(noEdges):
			noEdges = int (self.edgesEntry.get())
			if (noEdges < 3):
				tkMessageBox.showwarning("Warning","Entry for edges is less than 3.")
				return
			if (noEdges < (noNodes-1)):
				tkMessageBox.showwarning("Warning","Entry for edges must be enough for a tree structure. Needs %d." %(noNodes-1))
				return
			if (noEdges > (noNodes*(noNodes-1))/2)  :
				tkMessageBox.showwarning("Warning","Entry for edges provided is more than a complete graph." )
				return
		else:
			tkMessageBox.showwarning("Warning","Entry for edges is not an integer.")
			return

#noNodes, noEdges
		self.cg = LM.LexM(noNodes, noEdges)
		self.cg.createAG()

		self.G = True

	def onViewCGClick(self):
		"""function to call plotCompleteGraph to draw complete graph"""
		if self.G:
			#self.cg.plotCompleteGraph(self.cg.G)
			self.cg.plotWhole(self.cg.G, 1)
		else:
			tkMessageBox.showwarning("Warning","Create Arbitrary Graph first to view Arbitrary Graph.")
			return


	def onCreateNCGClick(self):

		if self.G:
			self.cg.createChrdG()
			self.G = True
		#else:
		#	tkMessageBox.showwarning("Warning","Create Arbitrary Graph first before create Chordal Graph.")
			return


	def onViewNCGClick(self):
		if self.G:
			
			#self.cg.plotFG(self.Ncg)
			self.cg.plotWhole(self.cg.G, 2)
		#else:
		#	tkMessageBox.showwarning("Warning","Create Nearly Chordal Graph first to view Nearly Chordal Graph.")
			return

	def onDisplayResultClick(self):
		if self.G:
			self.cg.finalDisplay()
			return

def center(toplevel):
	"""function to compute the center of the screen and place the window in the center"""
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
	x = w/2 - size[0]/2
	y = h/2 - size[1]/2
	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

if __name__ == "__main__":
	"""main function: the starting point of this weakly chordal graph generation method"""
	app = gui_tk(None)
	app.title("LExM Chordal Graph Generation")  
	app.geometry('350x250')#window size
	center(app)
	app.mainloop()
	app.quit()