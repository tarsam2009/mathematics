'''module graph

This module contains classes and definitions to explore elements of Graph
Theory. The most important element of this module is the Graph class. This
creates a graph stored with an adjacency list, thus allowing quick access,
but suffering from larger memory requirements. All helper functions
assume that the graph is provided from this class, which guarantess the
proper addition and removal of elements to and from the graph.
'''

import copy
from collections import deque
import string
import math

#==================
# CLASS DEFINITIONS
#==================
class Graph:
	'''
	class Graph

	The Graph class represents a graph as an adjacency list. Vertices
	and edges can be removed and added to this graph. Manipulations
	in excess of this require an outside method.
	'''
	def __init__( self ):
		'''Graph.__init__( self )

		Constructs an empty graph. The constuctor only generates
		empty graphs, but the Graph.load( file ) method allows
		the loading of a graph from a file.
		'''

		#A container for all vertices
		self.vertices = set()

		#A map of a vertex to all other vertices connected with a directed edge
		self.edge_map = dict()

		#A map of each edge to its weight
		self.edges = dict()
	
	def add_vertex( self, vertex ):
		'''Graph.add_vertex( vertex )

		Adds a hashable vertex to the graph. The vertex is
		given no edges.
		'''
		if not vertex in self.vertices:
			self.vertices.add( vertex )
			self.edge_map[vertex] = set()
	
	def remove_vertex( self, vertex ):
		'''Graph.remove_vertex( vertex )

		Removes a vertex from the graph. If the vertex is not
		in the graph, then no modifications are made. If the
		vertex is in the graph, then the vertex, as well as
		all edges connected to the vertex are removed from the
		graph.
		'''
		if vertex in self.vertices:
			self.vertices.remove( vertex )
			
			good_edges = dict()
			for edge in self.edges:
				if vertex in edge:
					self.edge_map[edge[0]].remove(edge[1])
				else:
					good_edges[edge] = self.edges[edge]

			del self.edge_map[vertex]
			self.edges = good_edges 

	def add_edge( self, vertex_a, vertex_b, weight=1 ):
		'''Graph.add_edge( a, b, weight )

		If a and b are in the graph and the edge from a to b, 
		denoted (a,b), is not already present in the graph, then
		add (a,b) to the graph. If no edge weight is specified,
		then the weight is assumed to be 1.
		'''
		if not (vertex_a, vertex_b) in self.edges and vertex_a in self.vertices and vertex_b in self.vertices:
			self.edges[(vertex_a,vertex_b)] = weight
			self.edge_map[vertex_a].add(vertex_b)
	
	def remove_edge( self, edge ):
		'''Graph.remove_edge( edge )
		
		If the edge, represented as a 2-ple is in the graph, then
		that edge is removed. This method properly removes all
		references to the edge from all storage places.
		'''
		if edge in self.edges:
			del self.edges[edge]
			self.edge_map[ edge[0] ].remove( edge[1] )

#===================
# METHOD DEFINITIONS
#===================
def disconnected_components(graph):
	'''disconnected_components( graph )
	
	Input: an instance of Graph
	Output: a list of the disconnected components of the graph

	Uses BFS to determine which segments of the graph are connected.

	ASSUMES THE GRAPH IS UNDIRECTED
	'''
	
	explored = set()
	clusters = list()
	
	#Outer cluster loop
	for vertex in graph.vertices:
		
		if vertex in explored:
			continue
			
		queue = deque()
		queue.append(vertex)
		
		cluster = set()
		cluster.add(vertex)
		
		#Find all the vertexes in the cluster
		while len(queue) > 0:
			tmp_vertex = queue.popleft()
			for edge_vertex in graph.edge_map[tmp_vertex]:
				if edge_vertex not in explored:
					explored.add(edge_vertex)
					queue.append(edge_vertex)
					cluster.add(edge_vertex)
		
		clusters.append(cluster)
	
	return clusters
