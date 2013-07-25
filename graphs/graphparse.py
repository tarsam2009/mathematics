'''module graphparse
This module handles the decoding of graphs from JSON data
CSV data into a graph as described in the graph module. Also
conversions into Octave data, Tikz pictures, and upload
files for the GAE are contained as well
'''

import json
import csv

def prepareUpload(graph, clusters, filepath):
    '''Given a graph and the clusters, this file output the JSON
    file that is to be read by the GAE server and used for
    recommendations. The output file will be saved in the folder
    designated by "filepath"

    USES: json
    '''
    
    data = dict()
    
    #Prepare the preferences list
    for vertex in graph['vertexes']:
        data[str(vertex)] = dict()
        
        #Clear to zero
        prefs = [0] * len(clusters)
        
        #For each vertex this is connected to
        for edge in graph['edges'][vertex]:
            #increment cluster friends for edge's cluster
            for i in xrange(0,len(clusters)):
                if edge in clusters[i]:
                    prefs[i] += 1
                    break
                    
        #increment cluster that vertex belongs to
        for i in xrange(0, len(clusters)):
            if vertex in clusters[i]:
                prefs[i] += 1
                break
            
        #Divide each value by the number of friends
        for i in xrange(0,len(clusters)):
            prefs[i] /= float(len(graph['edges'][vertex]) + 1)
            
        data[str(vertex)]['prefs'] = prefs
        
    #Set which cluster each vertex belongs to
    for i in xrange(0, len(clusters)):
        for vertex in clusters[i]:
            data[str(vertex)]['cluster'] = i
    
    with open(filepath + 'uploadfile', 'w') as f:
    
        data['clusters'] = list()
        
        for cluster in clusters:
            data['clusters'].append(list(cluster))
        
        keys = list()
        
        with open(filepath + 'key') as tmpfile:
            keys = tmpfile.readline().split(' ')
            
        pairs = list()

        with open(filepath + 'solution.mat') as tmpfile:
            pairs = [float( value ) for value in tmpfile.readline().split(' ')]

        result = sorted(zip(pairs, keys))
        
        sets = list()
        tmpset = set()
        previous = -1
        
        for pair in result:
            tmpset.add(pair[1])
            if pair[0] > previous:
                    sets.append(list(tmpset))
                    tmpset = set()
            previous = pair[0]

        sets.append(list(tmpset))
        
        data['markovorder'] = sets;
        
        json.dump(data, f)
    
def parse_csv(filepath):
    '''Attempts to parse the given filename from a CSV file
    into a graph described by the graph module. These files are
    created from Bulkloader downloads.
    '''
    print 'Parsing CSV file:', filepath
    
    grph = dict()
    grph['vertexes'] = set()
    grph['edges'] = dict()
    
    friends = dict()
    
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            if row[0] == 'idNum':
                continue

            grph['vertexes'].add(long(row[0]))
            friends[long(row[0])] = {long(n) for n in row[1].strip('[]"').split(',')}
            #print len(friends[long(row[0])])
        f.close()

    for vertex in grph['vertexes']:
        grph['edges'][vertex] = grph['vertexes'] & friends[vertex]
        
    #Validate symmetry
    for vertex,friends in grph['edges'].iteritems():
        for friend in set(friends):
            if not vertex in grph['edges'][friend]:
                grph['edges'][friend].add(vertex)
                
    return grph

def parse_json(filepath):
    '''Attempts to parse the given filename from a JSON file
    into a graph described by the graph module. These files are
    created from the Administration Downloads page.

    DEPRECATED: Downloaded files should be CVS.

    USES: json
    '''
    #PARSE JSON OBJECT FROM FILE
    print 'Parsing JSON file: ',filepath

    f = open(filepath, 'r')

    jsonfile = json.load(f)

    #print jsonfile

    #CONVERT JSON TO PERTINENT GRAPH

    graph = dict()

    graph['vertexes'] = set()
    graph['edges'] = dict()

    #Copy Vertexes
    for v in jsonfile['data']:
        graph['vertexes'].add(long(v['id']))
        
    #Copy Pertinent Edges
    for v in jsonfile['data']:
        tmpSet = set()
        for e in v['friends']:
            if long(e) in graph['vertexes']:
                tmpSet.add(long(e))
        
        graph['edges'][long(v['id'])] = tmpSet
        
    return graph
    
def storeResults(results, basedir):
    '''Stores the debug data contained in the results variable
    returned from the "graphcluster.cluster" method. This data
    can be loaded into Octave and plotted.
    '''
    fileA = open(basedir + 'xvals.txt', 'w')
    fileB = open(basedir + 'yvals.txt', 'w')

    for datum in results[1]:
        fileA.write(str(datum[0]) + '\n')
        fileB.write(str(datum[1]) + '\n')
        
    fileA.close()
    fileB.close()
    
def toOctaveFile(graph, components,  filepath ):
    '''This method converts the graph with the given disconnected
    components into a format that the Markov Octave script can
    interpret to produce the ordering.
    '''
    verts = list(graph['vertexes'])
    
    vertlen = len(verts)
    
    array = [ [int(e in graph['edges'][v]) for e in verts]for v in verts]
    
    with open(filepath + 'array', 'w') as f:
        for row in array:
            for i in xrange(vertlen):
                f.write(str(row[i]))
                if not i == vertlen - 1:
                    f.write(' ')
            
            f.write('\n')
            
    with open(filepath + 'trials', 'w') as f:
        for component in components:
            vert = None
            
            for item in component:
                vert = item
                break
                
            f.write(str(verts.index(vert) + 1) + ' ' + str(len(component)) + '\n')
    
    with open(filepath + 'key', 'w') as f:
        f.write(' '.join(str(vert) for vert in verts))
        

