'''module graphcluster
The methods in the module perform edge-betweenness clustering.

USES: graph, collections, itertools, operator, copy
'''

from graph import disconnectedComponents
from collections import deque
from itertools import combinations
import operator
import copy

#-----------------------------------------------------------

def suggestedModularity(clusters, basegraph):
'''If given a graph whose components give the clusters,
it calculates the modularity suggested by Newman and
Girvan when they introduced edge betweenness clustering
in 2003.
'''
    modularity = 0
    
    #Calculate total edges
    edgeCount = 0
    
    for vertex in basegraph['vertexes']:
        for edge in basegraph['edges'][vertex]:
            edgeCount += 1
            
    edgeCount /= float(2)
    
    #Create the matrix e
    
    e = list()
    for i in xrange(0, len(clusters)):
      e.append([0] * len(clusters))
    
    #Populate e
    for i in xrange(0, len(clusters)):
      for j in xrange(0, len(clusters)):
        value = 0
        for vert in clusters[i]:
          for edge in basegraph['edges'][vert]:
            if edge in clusters[j]:
                value += 1
        
        value /= (float(2) * edgeCount)
        e[i][j] = value
        
    #Calculate the Newman-Girvan modularity
    for i in xrange(0, len(clusters)):
       tmpValue = 0
       for j in xrange(0, len(clusters)):
         tmpValue += e[i][j]
       
       modularity += e[i][i] - (tmpValue * tmpValue)
          
    return modularity
    
#-----------------------------------------------------------
    
def cluster(graph, modularity=suggestedModularity):
'''When given a graph, this method performs edge-betweenness
clustering based on the provided modularity, which by default
is the suggestedModularity method. This method returns a
results list where

result[0] is the cluster that maximizes the modularity
result[1] is the value of each clustering's modularity
result[2] contains hierarchy data and is deprecated.
'''
    #Calculate Number of edges
    edgeCount = 0
    
    #If we add all the edges to a set, duplicates won't be
    #counted
    edgeSet = set()
    for vertex in graph['vertexes']:
        for toVertex in graph['edges'][vertex]:
            edgeSet.add(frozenset([vertex, toVertex]))
    
    edgeValues = dict()
    for edge in edgeSet:
        edgeValues[edge] = 0
    
    edgeCount = len(edgeSet)
    
    bestClusters = disconnectedComponents(graph)
    bestModularity = modularity(bestClusters, graph)
    previousClusters = bestClusters
    
    tmpgraph = copy.deepcopy(graph)
    
    updateEdgeValues(graph['vertexes'], graph, edgeValues)
    
    #For Debugging and nice pictures, include cut data
    cutData = [0] * (edgeCount + 1)
    cutData[0] = [len(bestClusters), bestModularity]
    
    #For pretty pictures, add hierarchical history
    hierarchy = list()
    hierarchy.append(bestClusters)
    clusterCount = len(bestClusters)
    
    #For each edge we have
    for i in xrange(0, edgeCount):
    	#Remove the most necessary edge (we store it in
    	#lostEdge for debugging reasons
        lostEdge = removeMostTraversedEdge(tmpgraph, edgeValues)
        clusters = disconnectedComponents(tmpgraph)
        
        #Update hierarchy
        if len(clusters) > clusterCount:
            hierarchy.append(clusters)
            clusterCount = len(clusters)
        
        tmpModularity = modularity(clusters, graph)

        if tmpModularity > bestModularity:
            bestModularity = tmpModularity
            bestClusters = clusters
        
        #This next section is an improvement not discussed
        #in the paper since it doesn't decrease the runtime
        #complexity. Only the edges in a cluster that has
        #broken into two need to have their edge betweenness
        #reevaluated.
        reevaluate = set()
        
        for cluster in clusters:
            if lostEdge[0] in cluster or lostEdge[1] in cluster:
                reevaluate |= cluster
        
        updateEdgeValues(reevaluate, tmpgraph, edgeValues)
        cutData[i + 1] = [len(clusters), tmpModularity] 
    
    return [bestClusters, cutData, hierarchy]

#-----------------------------------------------------------

def updateEdgeValues(vertexes, graph, edgeValues):
'''When given a set of vertices of a graph, this method
updates the values in edgeValues for edge-betweenness.
'''
    combinationGenerator = combinations(vertexes, 2)
    
    try:
        while True:
            test = frozenset(combinationGenerator.next())
            if test in edgeValues:
                edgeValues[test] = 0
    except StopIteration:
        pass
        
    
    combinationGenerator = combinations(vertexes, 2)
    
    try: 
        while True:
            pair = combinationGenerator.next()
            
            #Calculate the shortest paths 
            paths = allShortestPaths(graph,pair[0],pair[1])
            
            if len(paths) == 0:
                continue
            
            #Calculate value to give to edges
            value = 1 / float(len(paths))
            #print 'Path for',pair,'is',paths
            for path in paths:
                for i in xrange(0,len(path)-1):
                    edge = frozenset([path[i],path[i + 1]])
                    #print '\tEdge',edge
                    #Increment usage of each edge in path
                    edgeValues[edge] += value
    except StopIteration:
        pass #Do nothing when done
        
    #No return value since changes made in reference
            
#-----------------------------------------------------------

def removeMostTraversedEdge(graph, edgeValues):
'''Given a graph and all the edge weights of that graph,
it removes the edge with the highest betweenness value.
'''
mostUsed = max(edgeValues.iteritems(), key=operator.itemgetter(1))[0]
mostUsedList = list(mostUsed)

    #print 'Removing edge', mostUsed
    removeUndirectedEdge(graph, mostUsedList[0], mostUsedList[1])
    
    del edgeValues[mostUsed]
    
    return mostUsedList
        
#-----------------------------------------------------------

def densityModularity(graph, basegraph):
'''
DEPRECATED
If given an undirected graph, it computes the modularity
of the graph by first, computing all the clusters of the
graph. For each cluster, it counts the number of
internal edges twice, then divides it by the number of
vertexes, thus resembling the average inner edge count
per vertex. The final modularity is given by summing
over the modularities of the clusters.

NOTE: This was a custom made modularity and did not work well
'''
    clusters = disconnectedComponents(graph)
    
    modularity = 0
    
    for cluster in clusters:
        #print 'Modularity for cluster', cluster
        clusterModularity = 0
        for vertex in cluster:
            for toVertex in graph['edges'][vertex]:
                if toVertex in cluster:
                    clusterModularity+=1
        
        clusterModularity /= float(len(cluster))
        modularity += clusterModularity
    
    return modularity

#-----------------------------------------------------------

def removeUndirectedEdge(graph, a, b):
'''If given an undirected graph, it removes the connections
between the vertexes a and b. If the edge does not
exist or is directed, then a KeyError will be thrown.
'''
    graph['edges'][a].remove(b)
    graph['edges'][b].remove(a)

#-----------------------------------------------------------

def allShortestPaths(graph, start, end):
'''If given a graph that is undirected and a path exists 
between the start and end vertexes, this method is 
guaranteed to return a list containing all the
shortest paths.

graph - undirected graph
start - vertex to start the search from
end - vertex to finish at

Returns a list of all shortest paths from start to end.
'''

    #print 'Shortest paths from {0} to {1}'.format(start,end)
    explored = set()
    distance = dict()
    queue = deque()
    
    #Place default values in dictionary
    for vertex in graph['vertexes']:
        distance[vertex] = -2    

    explored.add(start)
    queue.append(start)
    distance[start] = 0
    
    #BFS to label distances to vertices up to the end vertex
    while queue:
        vertex = queue.popleft()
        
        if vertex == end:
            break
            
        for toVertex in graph['edges'][vertex]:
            
            if toVertex not in explored:
                explored.add(toVertex)
                distance[toVertex] = distance[vertex] + 1
                queue.append(toVertex)

    #print 'DISTANCES', distance
            
    #Reverse BFS on labeled vertices to build all paths    
    pathQueue = deque()
    pathQueue.append([end])
    shortestPaths = list()
    
    while pathQueue:
        #print '\tQUEUE', pathQueue
        path = pathQueue.popleft()
        
        vertex = path[0]
        #print 'CHECKING PATH', path
        for toVertex in graph['edges'][vertex]:
            
            if distance[toVertex] == (distance[vertex] - 1):
                
                #print '\tAPPENDING ELEMENT', toVertex
                newpath = list(path)
                newpath.insert(0, toVertex)
                
                if toVertex == start:
                    shortestPaths.append(newpath)
                else:
                    pathQueue.append(newpath)
                
                
    return shortestPaths
#-----------------------------------------------------------

def badModularity(graph, clusters):
'''DEPRECATED

As discussed in the paper, this modularity will not provide
good clusters and is included to help my check my own
calculations with the modularity.
'''
	modularity = 0
	for cluster in clusters:
		print 'Examaning cluster', clusters
		for v in cluster:
			print '\tLooking at vertex',v
			for toVertex in graph['edges'][v]:
				if toVertex in cluster:
					print '\t\tSame cluster as',toVertex
					modularity = modularity + 1
				else:
					print '\t\tDifferent cluster as', toVertex
					modularity = modularity - 1
	
	return modularity

def generateFigure():
'''Creates a graph as described in the graph module that 
creates the full graph of the figure in the paper that
shows the need for a modularity.'''
	graph = dict()
	graph['vertexes'] = set(range(10))
	graph['edges'] = dict()
	graph['edges'][0] = set([1,2])
	graph['edges'][1] = set([0,2])
	graph['edges'][2] = set([0,1,3])
	graph['edges'][3] = set([2,4,5,6])
	graph['edges'][4] = set([3,5,6])
	graph['edges'][5] = set([3,4,6,7])
	graph['edges'][6] = set([3,4,5])
	graph['edges'][7] = set([5,8,9])
	graph['edges'][8] = set([7,9])
	graph['edges'][9] = set([7,8])
	
	return graph
