#This script was initially used to produce the FBS proof
#of concept figure.

#Prepare global variables

f = open('sportsgraph/fbs2012teams.txt')

grph = dict()
grph['vertexes'] = set()
grph['edges'] = dict()


teamName = dict()
confMap = dict()
confName = dict()

#Read in the team names and correct conferences

for line in f:
    data = line.split()
    
    index = int(data[0])
    
    #Add vertex and empty edge set to graph
    grph['vertexes'].add(index)
    grph['edges'][index] = set()
    
    #Add naming attributes for later
    confMap[index] = int(data[1])
    
    teamName[index] = data[2]
    confName[int(data[1])] = data[3]

f.close()

#Set the color map
colorlist = ['Red','Blue','Green','BlueGreen', 'Tan', 'Yellow',
             'SkyBlue', 'Gray', 'BrickRed', 'OrangeRed', 'BurntOrange', 'Mulberry']
             
colorMap = dict()

for vert in grph['vertexes']:
    colorMap[vert] = colorlist[confMap[vert] - 1]


#Read in the correct edges

f = open('sportsgraph/fbs2012games.txt')

for line in f:
    data = line.split()
    
    teamA = int(data[0])
    teamB = int(data[1])
    
    grph['edges'][teamA].add(teamB)
    grph['edges'][teamB].add(teamA)
    
f.close()

#Now, cluster the graph

import graphcluster
import graphparse
import graph

results = graphcluster.cluster(grph)

graphparse.storeResults(results, '/home/michael/Desktop/')

f = open('/home/michael/Documents/Carson-Newman/Honors Project/Images/DataGraphs/Hierarchies/testhierarchy/sporthierarchy', 'w')

f.write( graph.toLatexClusters(results[0], grph, colorMap, confName, colorlist))

f.close()
