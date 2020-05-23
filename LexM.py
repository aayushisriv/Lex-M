"""
@author- Aayushi Srivastava
This code performs LEx-M as mentioned in the paper of Pinar Heggernes: Minimal Triangulations of graphs: A survey
"""

from operator import itemgetter
import numpy as np
# pandas as pd
import random
import numpy as np

import itertools
import copy
#import collections

from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class LexM:

	def __init__(self, noNodes, noEdges):
		self.noNodes = noNodes
		self.noEdges = noEdges
		self.G = {}
		#self.H = {}
		#self.S = []
		self.vertexList = [] #original vertexList
		self.GEdgeList = []
		#self.HEdgeList = []
		self.F = []
		self.fc = 0
		#self.sc = 0
		#self.alpha = [] #list for number of vertices
		self.unnumberedVertices = [] #list for vertices yet to be numbered
		self.numberedVertices = [] #list for the vertices numbered
		self.LabelsDict = {} #Dictionary with vertex as key and labels as value
		self.NumberDict = {} #Dictionary with vertexas key and number as value


		self.meo = []#Minimal elimination ordering
		self.Fill = []#Fill edges


	def createAG(self): 
		"""function to create arbitrary graph"""
		self.G = nx.dense_gnm_random_graph(self.noNodes, self.noEdges)
		#self.G = {0: [2, 3, 5], 1: [9, 2, 3], 2: [0, 1, 3, 5], 3: [0, 1, 2, 9], 4: [8, 5, 6], 5: [0, 2, 4, 6], 6: [9, 4, 5], 7: [8], 8: [4, 7], 9: [1, 3, 6]}
		self.G = { 0: [1, 2, 4],
				   1: [0, 4],
				   2: [0, 3],
				   3: [2, 5],
				   4: [0, 1, 5],
				   5: [3, 4]}
		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
				
		for i in range(0, self.noNodes):
			self.vertexList.append(i)
		for key, value in self.G.iteritems():
			for v in value:
				if key<v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		
		self.G = nx.Graph(self.G)
		connComp = sorted(nx.connected_components(self.G))
		self.G = nx.to_dict_of_lists(self.G)
		
		connComp = list(connComp)
		noOFConnComp = len(connComp)
		if noOFConnComp > 1:
			#print "Here we are"
			print connComp
			self.G = nx.Graph(self.G)
			#self.plotArbitraryGraph(self.G)
			j = 0
			while j < noOFConnComp - 1:
				u = random.choice(list(connComp[j%noOFConnComp]))
				v = random.choice(list(connComp[(j+1)%noOFConnComp]))
				self.addAnEdge(self.G, self.GEdgeList, u, v)
				j = j + 1
		print str(self.G)
		self.G = nx.Graph(self.G)
		#self.plotArbitraryGraph(self.G)
		#print "see"
		self.G = nx.to_dict_of_lists(self.G)
		#self.HEdgeList = copy.deepcopy(self.GEdgeList)
		#self.H = copy.deepcopy(self.G)#making copy of graph G
		self.unnumberedVertices = copy.deepcopy(self.vertexList)
		#self.lexm(self.H ,self.HEdgeList)#LexM Function
		#self.FinalGraph(self.G,self.Fill, self.vertexList)#to plot chordal graph
		
	def addAnEdge(self, graphToAdd, edgeListToAdd, v1, v2):
		"""function to add an edge in the graph,used in case of unconnected arbitrary graph only"""
		graphToAdd = nx.to_dict_of_lists(graphToAdd)
		graphToAdd[v1].append(v2)
		graphToAdd[v2].append(v1)
		e = []
		e.append(v1)
		e.append(v2)
		edgeListToAdd.append(e)

	def plotArbitraryGraph(self, graphToDraw):
		"""function to plot arbitrary graph"""
		#graphToDraw = nx.to_dict_of_lists(graphToDraw)
		edges = 0
		for node, degree in graphToDraw.iteritems():
			edges += len(degree) 
		#print type(self.G)
		#print self.G
		#self.HEdgeList = copy.deepcopy(self.GEdgeList)
		#self.H = copy.deepcopy(self.G)
		
		#print self.H
		graphToDraw = nx.Graph(graphToDraw)
		GD = nx.Graph(graphToDraw)
		pos = nx.spring_layout(GD)

		print "\nArbitrary Graph: "+str(self.G)
		print "\nNo. of edges in the Arbitrary Graph: "+ str(edges/2)

		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_nodes(GD, pos, node_color='red', node_size=300, alpha=0.8)
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()

	def createChrdG(self):
		#self.HEdgeList = copy.deepcopy(self.GEdgeList)
		#self.H = copy.deepcopy(self.G)
		#self.H = nx.Graph(self.H)
		print "My Edgelist:",self.GEdgeList

		print "Start LexM"
		self.lexm(self.G ,self.GEdgeList)#LexM Function
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)--com
		print "End Lex M"
		return True
		#self.FinalGraph(self.G,self.NEdgeList,self.vertexList)


	def lexm (self,graphC,EdgList):
	#Lex M"
		graphC = nx.Graph(graphC)
		#declared empty label dictionary and numbered vertices dictionary
		keys = self.vertexList
		self.LabelsDict = {k: [] for k in keys} #(self.vertexList, []) #l(v)=Null
		self.NumberDict = dict.fromkeys(self.vertexList, None)
		rankv = self.noNodes #ranks given to vertices
			
		r = (len(self.unnumberedVertices) -1)
		for v in range(r, 0, -1):
			S = []
			if  v == r: #first iteration to choose arbitrary last vertex and give it rank n
				print "Starting V ",v
				
				self.LabelsDict[v]  = [] 
				self.NumberDict[v] = self.noNodes #alpha(v) = i

				self.fc = v # removing this vertex from unnumbered vertex list to numbered vertex list
				self.unnumberedVertices.remove(self.fc)
				self.numberedVertices.append(self.fc)


				print "Vertex starting with",v

				#other iterations
			else:
				print "UL in next iteration", self.unnumberedVertices
				#finding vertex v of lexicographically maximum label in every iteration
				mat = max((len(ve), k) for k,ve in self.LabelsDict.iteritems() if k in self.unnumberedVertices)[1:]

				v = mat[0]
				print "Vertex Selected (v):",v
				

				rankv = rankv -1

			for u in self.unnumberedVertices:
				#u = random.choice(self.unnumberedVertices)
				if u != v:
					print "U is:",u
					#S = [] #list S will be updated with every new vertex
					dep = []
					dep.append(v)
					#dep.append(self.fc)
					dep.append(u)
					nbc = list(itertools.combinations(dep,2))#list containg u,v as tuples p
					#print "Dekho v",self.unnumberedVertices
						
					for p in nbc:
						
						v1 = p[0]
						v2 = p[1]
					#if there is an edge uv or path u,.....,v
					self.G = nx.Graph(self.G)
					if (self.G.has_edge(*p)) or (nx.has_path(self.G,v,u)):
						#S.append(u)
						#rankv = rankv - 1
						if self.G.has_edge(*p):
							print "Already Edge is there",p
							S.append(u)
						#CEd = self.G.edges([v]) #all the vertices that has edge with u
						#print "Found the uv edge", CEd
						#S.append(u)
						
						#print "Inter",FList
						#for j in CEd:
							#print p[1]
							#S.append(p[1]) #Adding all the vertices which have edge with u

						#print "S due to edge became:",S
						#Path checking
						#print "Check if there is a path",p
						#for pt in self.unnumberedVertices:
						if (nx.has_path(self.G,u,v)):
							#print "Path between",u,"and",v
							paths = nx.all_simple_paths(self.G, source=u, target=v)#gives all simple paths between u and v
							dps = (list(paths))
							#print "Found",dps
							if dps:
								uval = self.LabelsDict.get(u)#u's label list
								#bc = self.LabelsDict.get(v) #v's label list
								#ulex = 0
								#if uval != None:
								ulex = len(list(filter(bool,uval)))#lexig length of label of u

								#vtc = 0
								#if bc != None:
									#vtc = len(list(filter(bool,bc)))#lexig length of label of v


								#print "Lexicographic label length of u:",u,"is:",ulex
								

								for plist in dps:
									g = len(plist)
									count = 0
									#print "Checking path for:",plist
									for x in range(1, g-1):
										
										xval = self.LabelsDict.get(plist[x])
										xlex = len(list(filter(bool,xval)))
										#print "Lexicographic length of x",plist[x],"is:",xlex
										if (plist[x] in self.unnumberedVertices) and (xlex < ulex):
											count += 1

									if (count == (g-2)) and (count != 0) and ((g-2) != 0):
										#if (count == (g-2)):
										#print "Consider the path:",plist
										S.append(u)
									#print "S due to path",list(set(S))




									#for x in plist:
									#	count = 0
									#	if (x != u) and (x !=v):
									#		#print "Vertices in path:", x
									#		xval = self.LabelsDict.get(x)
									#		#xlex = 0
									#		#if xval != None:
									#		xlex = len(list(filter(bool,xval)))
									#		print "Lexicographic length of x:",x,"is:",xlex

									#		if (x in self.unnumberedVertices) and (xlex < ulex):
									#			count += 1
									#		#print "The ver",count
									#		if (count != 0) and ((g-2) != 0):
									#			if (count == (g-2)):
									#				print "count", count
									#				print "g-2",(g-2)
									#				print "Consider this path:",plist
									#				#S = S + plist
									#				S.append(u)
											#print "S due to path:",S
											#elif count < (len(plist)-2):
										
							#S.append(u)
						else:
							print "No path between uv"


					
					#pathlist = [node for sbl in dps for node in sbl if node in self.unnumberedVertices]
					
					#Finding if l(xi) is lexicographically smaller than l(u)
		
							
				else:
					print "Consider another unnumbered vertex u"
					continue




				Sd = list(set(self.unnumberedVertices) & set(S)) #final S excluding numbered vertices
				#Sd = list(set(S))
				print "S to consider is Sd:",Sd
				
				#vert = 0 Making label dictionary
				#if v != r:
				#	self.LabelsDict[v].append(rankv)

				#Third Loop for fill edges and rank	
			print "final s for:",v,"is:",S
			
			#Removing vertex from unnumbered list and adding to numbered
			#if r == 1:
			#	print "LAst v:",v
			if v != r:
				self.unnumberedVertices.remove(v)
					#dbl.remove(tempu)
				#print "My num list", self.numberedVertices
				self.numberedVertices.append(v)

			#Adding LAbels to Label Dictionary
			for vert in Sd:
				#print vert
				#if vert in self.LabelsDict:
				#if vert in self.unnumberedVertices:
				if rankv not in self.LabelsDict[vert]:
					self.LabelsDict[vert].append(rankv)
					
			
			print self.LabelsDict
		
			#Making Fill edges between u and v, ut is the vertices in S ie. Sd
			
			for ut in Sd:
				#if ut in self.unnumberedVertices:
				print "Start for fill edges:", Sd
				print "Edges are:",v,"and",ut
				if (v != ut): #ut is unnnumbered vertex in S to avoid self loops
				#Scomb = list(itertools.combinations(FList,2))
					if self.G.has_edge(v,ut):
						print "uv belongs to Edgelist:"
					#continue
					else:
						#print "Vkl"
					#	graphC.add_edge(v,ut)
						#self.Fill.append(u)
						self.Fill.append((v,ut))
						print "Added Edge as uv does not belong to EdgeList:", v,ut
						#if [v,ut] or [ut,v] in self.GEdgeList:
						#	print "uv edge is present in edgelist",ut,v
						#else:


					print "Fill edges added are", self.Fill

						
			self.NumberDict[v] =  rankv#alpha(v) = i
				#v = self.fc

			# "My un list", self.unnumberedVertices

			#if v != r:
			#	self.unnumberedVertices.remove(v)
					#dbl.remove(tempu)
				#print "My num list", self.numberedVertices
			#	self.numberedVertices.append(v)
					#print "After My num list", self.numberedVertices
					
				#SList = list(set(S))
				#print "S due to path became",SList

			#Swapping
			#tempu = v
			#v = self.fc
			#self.fc = tempu


	def FinalGraph(self,graphVerify,newaddedgelist,vertexlist):
		print "EdgeList verifying",newaddedgelist
		print "Total Edges added in LexM is ",len(newaddedgelist)
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)

		B = copy.deepcopy(self.G)
		B = nx.Graph(B)
		B.add_nodes_from(vertexlist)
		B.add_edges_from(newaddedgelist)
		B = nx.to_dict_of_lists(B)
		print "see B", B
		##Recognition----
		graph = nx.Graph(B)
		print "We could"
		#print type(B)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else :
			print "NO IT IS NOT CHORDAL"

		#print "Draw graph"
		nx.draw_networkx_nodes(GD, pos, nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='Min degree')	
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='Min degree')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		plt.show()	

	def plotWhole(self,Fgrap,gname):
		plt.figure()
		if gname == 1:
			self.plotArbitraryGraph(self.G)
		elif gname ==2:
			self.FinalGraph(self.G, self.Fill, self.vertexList)

		



					#for t in S:




						#graphC.add_edge(*p)
						#print "Edge added",p
						#self.F.append(p)


			#S = [] #collecting all vertices whose labels are to change
			#for 
			#for v in self.unnumberedVertices:
				#if 

		
		#print "Displaying Vertex with Labels",self.LabelsDict
	def finalDisplay(self):

		if self.unnumberedVertices:
			
			self.numberedVertices = self.numberedVertices + self.unnumberedVertices
			
		for m in self.unnumberedVertices:
			self.NumberDict[m] = 1
			
			self.unnumberedVertices.remove(m)
		
		for k,v in self.LabelsDict.iteritems():
			v.sort()
			self.LabelsDict[k] = [item for item, _ in itertools.groupby(v)]
		
		print "Final Label Dictionary:", self.LabelsDict
		print "Number Dict",self.NumberDict
		print "Numbered Vertex List", self.numberedVertices
		print "Unnumbered Vertex List", self.unnumberedVertices
		print "Final Label Dictionary:", self.LabelsDict
		print "Edges added to make it chordal",self.Fill
		print "Number of edges added:",len(self.Fill)
		self.meo = self.numberedVertices[::-1]
		print "Minimal Elimination Ordering is:",self.meo



"""
val1 = int(raw_input("Enter no. of nodes:"))
val2 = int(raw_input("Enter no. of edges:"))
abc = LexM(val1,val2)
abc.createAG()
"""