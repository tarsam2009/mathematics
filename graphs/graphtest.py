"""module graphtest
This module was originally created to prepare test cases
for the clustering methods used later. However, these
methods were later deprecated."""

import graph
import graphcluster
import random

def create_test():
'''Creates a graph as described in the graph module that
represents Newman and Girvan's graph of the Karate Club.
'''
    graph = dict()
    graph['vertexes'] = range(1,35)
    
    graph['edges'] = dict()
    graph['edges'][1] = set([2,3,4,13,5,6,7,11,22,12,18,20,8,32,9])
    graph['edges'][2] = set([3,31,14,20,4,1,22,8,18])
    graph['edges'][3] = set([33,28,29,9,10,14,4,2,1,8])
    graph['edges'][4] = set([14,3,2,1,13])
    graph['edges'][5] = set([1,11,7])
    graph['edges'][6] = set([1,7,11,17])
    graph['edges'][7] = set([1,6,17,5])
    graph['edges'][8] = set([1,2,3])
    graph['edges'][9] = set([1,3,33,34,31])
    graph['edges'][10] = set([3,34])
    graph['edges'][11] = set([1,5,6])
    graph['edges'][12] = set([1])
    graph['edges'][13] = set([1,4])
    graph['edges'][14] = set([2,3,4,34])
    graph['edges'][15] = set([33,34])
    graph['edges'][16] = set([33,34])
    graph['edges'][17] = set([6,7])
    graph['edges'][18] = set([1,2])
    graph['edges'][19] = set([33,34])
    graph['edges'][20] = set([34,2,1])
    graph['edges'][21] = set([33,34])
    graph['edges'][22] = set([1,2])
    graph['edges'][23] = set([33,34])
    graph['edges'][24] = set([30,33,34,28,26])
    graph['edges'][25] = set([26,28,32])
    graph['edges'][26] = set([24,25,32])
    graph['edges'][27] = set([30,34])
    graph['edges'][28] = set([34,3,25,24])
    graph['edges'][29] = set([3,32])
    graph['edges'][30] = set([27,34,33,24])
    graph['edges'][31] = set([34,33,9,2])
    graph['edges'][32] = set([29,33,34,1,25,26])
    graph['edges'][33] = set([24,19,9,21,30,16,15,34,23,31,3,32])
    graph['edges'][34] = set([14,20,33,24,28,32,9,31,10,16,23,15,27,30,21,19])
    
    return graph

def generatePlantedL(vertCount, clusters, p=float(1),q=float(0)):
'''generatePlantedL( vertCount, clusters, p=1,q=0)
Create a test graph that contains "vertCount" vertices, has
"clusters" clusters, and the edges are placed where edges
have a "p" probability of being between edges in the same
cluster and a "q" probability of being between edges in
different clusters.

Uses: random
'''
    graph = dict()
    graph['vertexes'] = set(range(1, vertCount + 1))
    graph['edges'] = dict()
    
    verts = list(graph['vertexes'])
    
    for v in graph['vertexes']:
        graph['edges'][v] = set()
    
    for iindex in xrange(0,len(verts) - 1):
        i = verts[iindex]
        for jindex in xrange(iindex + 1, len(verts)):
            j = verts[jindex]
            if iindex % clusters == jindex % clusters:
                if random.random() <= p:
                    graph['edges'][i].add(j)
                    graph['edges'][j].add(i)
            else:
                if random.random() <= q:
                    graph['edges'][i].add(j)
                    graph['edges'][j].add(i)
    
    return graph
    
def plantedTrials(vertCount, clusters,
                  p=float(1), q=float(0),
                  maxTrials=100, subTrials=100, qstep=0):
'''Automates the testing of multiple plantedL graphs

Deprecated
'''
    data = [0] * maxTrials
    
    for i in xrange(0, maxTrials):
        trialValue = 0
        print 'Starting trial',i+1, 'with p={0},q={1}'.format(p,q)
        
        for j in xrange(0, subTrials):
            grph = generatePlantedL(vertCount, clusters,
                                    p, q)
            
            trialValue += len(graphcluster.cluster(grph))
        
        trialValue /= float(subTrials)
        
        data[i] = trialValue
        
        print '\tComplete'
        
        q += qstep
    return data
