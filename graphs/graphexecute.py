import argparse
from graphparse import parseGraph
import graphcluster
import graphtest
import copy

#PREPARE COMMAND LINE ARGUMENT
#parser = argparse.ArgumentParser(description='Graph Theory Time')

#parser.add_argument('file', metavar='f', type=str, help='The JSON encoded file.')

#args = parser.parse_args()

#graph.toLatex(parseGraph(args.file))

#grph = parseGraph(args.file)

#This section tests all shortest paths

graph = graphtest.generatePlantedL(50,5)

print graphcluster.cluster(graph)
