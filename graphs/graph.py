'''module graph

This module contains methods to find the components of a
graph and also to visual a graph with Tikz.

The data structure of 'graph' used in this file is as follows:
   a 'graph' is a dictionary with an entry 'vertexes' and
      'edges'
      
   'graph["vertexes"]' contains a set of the graphs vertices
   
   'graph["edges"]' contains a dictionary with entries for
      each vertex
   
   'graph["edges"][v] contains a set where each element in 
      the set implies the edge v to that element exists in
      the graph.
'''

import copy
from collections import deque
import string
import math

def disconnectedComponents(graph):
'''When given a graph, this method looks for the connected
components of the graph that are disconnected from each other
and returns the sets in a list.

USES: deque
'''
    explored = set()
    clusters = list()
    
    #Outer cluster loop
    for vertex in graph['vertexes']:
        
        if vertex in explored:
            continue
            
        queue = deque()
        queue.append(vertex)
        
        cluster = set()
        cluster.add(vertex)
        
        #Find all the vertexes in the cluster
        while len(queue) > 0:
            tmpVertex = queue.popleft()
            for edgeVertex in graph['edges'][tmpVertex]:
                if edgeVertex not in explored:
                    explored.add(edgeVertex)
                    queue.append(edgeVertex)
                    cluster.add(edgeVertex)
        
        clusters.append(cluster)
    
    return clusters

def toLatexHierarchy(vertexSet,clusterList):
'''INCOMPLETE

This method was initially created to create a Tikz hierarchy
in order to visual the clustering. However, it was not
required for the project and development was cancelled. It
remains here if further work is done.
'''
    height = 0.5
    width = 1
    
    f = open('/home/michael/Documents/Carson-Newman/Honors Project/Images/DataGraphs/Hierarchies/testhierarchy/sporthierarchy', 'w')
    
    f.write('''\documentclass{article}
\usepackage{tikz}

\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment{tikzpicture}
\setlength\PreviewBorder{5pt}

\\begin{document}
\\begin{tikzpicture}[thick]

\\tikzstyle{every node}=[fill=red!30,rounded corners]
\\tikzstyle{edge from parent}=[red,thick,draw]

''')
    
    f.write('''\\node {root}\n''' + subHierarchy(vertexSet, clusterList, 1) + ';')
    
    f.write('''
\\end{tikzpicture}
\\end{document}''')
    
    f.close()

def subHierarchy(cluster, clusterList, depth):
'''INCOMPLETE

For use by the toLatexHierarchy method only
'''
    result = ''
    tab = string.join(['    '] * depth)
    #print 'Creating sub hierarchy for ', cluster
    for smallerCluster in clusterList[depth]:
        #print '\tSubcluster of ', smallerCluster
        if smallerCluster.issubset(cluster):
            result += tab + 'child{'
            if len(smallerCluster) == 1:
                result += ' node{' + str(smallerCluster) + '}\n' + tab +'}'
            else:
                result += ' node{' + str(depth) + '}\n' + subHierarchy(smallerCluster, clusterList, depth + 1) + '\n}'

    return result
    
#-----------------------------------------------------------

def toLatexColoredClusters(clusters, graph, colorMap, confName, colorlist):
'''This method, when given clusters, a graph, a color map,
a cluster name mape, and a color list produces the figures
seen in the proof of concept figures in the final paper

USES: copy, math
'''
    result = '''\documentclass{article}
\usepackage{color}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{tikz}

\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment{tikzpicture}
\setlength\PreviewBorder{5pt}

\\begin{document}
\\newcommand{\circlediam}{2cm}
\\begin{tikzpicture}[thick]
\\tikzstyle{every node}=[circle,draw=black,fill=red] {};

'''
    centerStep = 360 / float(len(clusters))
    
    circleDiameter = '2cm'
    
    clusterindex = 0
    
    for i, cluster in enumerate(clusters):
        center = (math.cos(math.radians(centerStep * i)) * 12,
                  math.sin(math.radians(centerStep * i)) * 12)
        
        result += '\\begin{scope}' + '[xshift={0:.2f}cm, yshift={1:.2f}cm]'.format(center[0],center[1])
        
        size = float(len(cluster))
        step = 360 / size
        
        for j, vert in enumerate(cluster):
            result += '\t\\node [fill={4}] ({0}) at ({1}:{2}) {3};\n'.format(clusterindex,step * j,circleDiameter, '{}', colorMap[vert])
            clusterindex += 1
        
        result += '\\end{scope}'
        
    tmpgraph = copy.deepcopy(graph)
    vertlist = list(graph['vertexes'])
    
    for i in xrange(0,len(vertlist)):
        for j in tmpgraph['edges'][vertlist[i]]:
            tmpgraph['edges'][j].remove(vertlist[i])
            result += '\n\\draw ({0}) -- ({1});'.format(i,
               vertlist.index(j))
        
        
    prevConf = None
        
    for key in confName:
        name = confName[key]
        
        
        if not prevConf:
            result += '\n\\node [fill={0}, rectangle] ({1}) {2};'.format(colorlist[key-1], name, '{' + name + '}')
        else:
            result += '\n\\node [fill={0}, rectangle] ({1}) [below of={3}]{2};'.format(colorlist[key-1], name, '{' + name + '}', prevConf)
        
        prevConf = name
        
    result += '\n\n\\end{tikzpicture}\n\\end{document}'
        
    return result
    
#-----------------------------------------------------------

def toLatexClusters(clusters, graph):
'''This method, when given a set of clusters and a graph,
produces a Tikz picture that visualizes the graph as a
circle of clusters, each of which is a circle of the cluster's
vertices.

USER: copy, math
'''
    result = '''\documentclass{article}
\usepackage{color}
\usepackage[usenames,dvipsnames]{xcolor}
\usepackage{tikz}

\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment{tikzpicture}
\setlength\PreviewBorder{5pt}

\\begin{document}
\\newcommand{\circlediam}{2cm}
\\begin{tikzpicture}[thick]
\\tikzstyle{every node}=[circle,draw=black,fill=red] {};

'''
    centerStep = 360 / float(len(clusters))
    
    circleDiameter = '2cm'
    
    clusterindex = 0
    
    for i, cluster in enumerate(clusters):
        center = (math.cos(math.radians(centerStep * i)) * 4,
                  math.sin(math.radians(centerStep * i)) * 4)
        
        result += '\\begin{scope}' + '[xshift={0:.2f}cm, yshift={1:.2f}cm]'.format(center[0],center[1])
        
        size = float(len(cluster))
        step = 360 / size
        
        for j, vert in enumerate(cluster):
            result += '\t\\node ({0}) at ({1}:{2}) {3};\n'.format(vert,step * j,circleDiameter, '{}')
        
        result += '\\end{scope}'
        
    tmpgraph = copy.deepcopy(graph)
    vertlist = list(graph['vertexes'])
    
    for i in xrange(0,len(vertlist)):
        for j in tmpgraph['edges'][vertlist[i]]:
            tmpgraph['edges'][j].remove(vertlist[i])
            result += '\n\\draw ({0}) -- ({1});'.format(vertlist[i],
               j)

    result += '\n\n\\end{tikzpicture}\n\\end{document}'
        
    return result   
 
#-----------------------------------------------------------

def toLatex(graph):
'''This method, when given a graph, prints the contents of
a Tikz image that shows the graph with the vertices in a
circle.

USES: copy, math
'''
    vertlist = list(graph['vertexes'])
    tmpgraph = copy.deepcopy(graph)
    size = len(vertlist)
    circleDiameter = '4cm'
    step = 360 / size;
    result = '''\documentclass{article}
\usepackage{tikz}

\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment{tikzpicture}
\setlength\PreviewBorder{5pt}

\\begin{document}
\\newcommand{\circlediam}{2cm}
\\begin{tikzpicture}[thick]
\\tikzstyle{commonnode}=[circle,draw=black,fill=red] {};

'''
    for i in xrange(0,size):
        result += '\\node ({0}) at ({1}:{2}) [commonnode] {3};\n'.format(i,step * i,circleDiameter, '{}')
        
    for i in xrange(0,size):
        for j in tmpgraph['edges'][vertlist[i]]:
            tmpgraph['edges'][j].remove(vertlist[i])
            result += '\n\\draw ({0}) -- ({1});'.format(i,
               vertlist.index(j))
            
    result += '\n\n\\end{tikzpicture}\n\\end{document}'
    print result
