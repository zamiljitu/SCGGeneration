import random
import numpy as np

import itertools
import copy

import networkx as nx # used this only for converting "dictionary typed graph to networkx graph" for visualization with matplotlib
import matplotlib.pyplot as plt #python plotting library

class StronglyChordalGraph:
    """This class turns the trampoline into strongly chordal graph. During this process it generates a trampoline for the given 
    number of vertices and and the number of edges. Then generate strongly chordal graph."""
    
    def __init__(self, noNodes, noEdges):
        self.noNodes = noNodes
        self.compNodes = []
        self.indNodes = []
        self.noEdges = noEdges
        self.treeEdges = 0
        self.chordalTree = {}
        self.chordalGraph = {}
        self.stronglyChordalGraphMat = []
        self.stronglyChordalGraphDict = {}
        self.neighborhoodMatrix = []
        self.peoLookupDict = {}
        self.closedNeighborhood = {}
        self.recognitionSEO = []

    def createCG(self):
        """function to create trampoline"""
        
        #self.chordalGraph = { 0: [4, 7], #trampoline on n=4
                              #1: [4, 5],
                              #2: [5, 6],
                              #3: [6, 7],
                              #4: [0, 1, 5, 6, 7],
                              #5: [1, 2, 4, 6, 7],
                              #6: [2, 3, 4, 5, 7],
                              #7: [0, 3, 4, 5, 6]}
        
        #self.chordalGraph = { 0: [5, 9], #trampoline on n=5
                              #1: [5, 6],
                              #2: [6, 7],
                              #3: [7, 8],
                              #4: [8, 9],
                              #5: [0, 1, 6, 7, 8, 9],
                              #6: [1, 2, 5, 7, 8, 9],
                              #7: [2, 3, 5, 6, 8, 9],
                              #8: [3, 4, 5, 6, 7, 9],
                              #9: [0, 4, 5, 6, 7, 8]}
        
        #self.chordalGraph = {}
        allNodes = range(self.noNodes)
        self.compNodes = allNodes[:len(allNodes)//2]
        self.indNodes = allNodes[len(allNodes)//2:]
        
        cycleEdges = []
        
        for i in self.compNodes:
            j = i % len(self.compNodes)
            k = (i+1) % len(self.compNodes)
            e = []
            e.append(j)
            e.append(k)
            cycleEdges.append(e)
            if not self.chordalGraph:
                self.chordalGraph[j] = list()
                self.chordalGraph[j].append(k)
                self.chordalGraph[k] = list()
                self.chordalGraph[k].append(j)
            else:
                self.chordalGraph[j].append(k)
                if k not in self.chordalGraph:
                    self.chordalGraph[k] = list()
                self.chordalGraph[k].append(j)
        
        #cycleNodes, cycleEdges = self.createEdgeList(self.chordalGraph)
        
        for ce in range(len(cycleEdges)):
            for i in range(len(self.indNodes)):
                if ce == i:
                    for c in cycleEdges[ce]:
                        self.chordalGraph[c].append(self.indNodes[i])
                        if self.indNodes[i] not in self.chordalGraph:
                            self.chordalGraph[self.indNodes[i]] = list()                        
                        self.chordalGraph[self.indNodes[i]].append(c)
        
        allNodes, cyclePlusIndEdges = self.createEdgeList(self.chordalGraph)
        
        self.createCompleteGraph(self.compNodes, cyclePlusIndEdges, self.chordalGraph)
    
        #self.createSCG()
        return True        
    
    
    def createEdgeList(self, graph):
        """function to create node list and edge list from dictionary (adjacency list)"""
        nodeList = []
        edgeList = []
        for v1, v in graph.iteritems():
            nodeList.append(v1)
            for v2 in v:
                e = []
                if v1<v2:
                    e.append(v1)
                    e.append(v2)
                    edgeList.append(e)
        return nodeList, edgeList
    
    def createCompleteGraph(self, vertexList, edgeList, graph):
        """function to create complete graph on the set of vertices"""
        eCounter = 0
        for pair in itertools.combinations(vertexList, 2):
            v1 = pair[0]
            v2 = pair[1]
            if [v1, v2] not in edgeList and [v2, v1] not in edgeList:
                self.addAnEdge(graph, v1, v2)
                print "\nAdded edge between: "+str(v1)+" and "+str(v2)
                eCounter = eCounter + 1
        return eCounter
    
    def createSCG(self):
        """function to create strongly chordal graph by adding minimum number edges in a trampoline"""
        self.stronglyChordalGraphDict = copy.deepcopy(self.chordalGraph)
        
        alreadyChosen = []
        v1 = random.choice(list(set(self.indNodes).difference(set(alreadyChosen))))
        #v1 = 5
        alreadyChosen.append(v1)
        neighborsOfV1 = self.chordalGraph.get(v1)
        notNeighborsOfV1 = list(set(self.compNodes).difference(set(neighborsOfV1)))
        for v2 in notNeighborsOfV1:
            self.addAnEdge(self.stronglyChordalGraphDict, v1, v2)
            print "\nAdded edge between: "+str(v1)+" and "+str(v2)
            #self.plotSCG("Added edge between: "+str(v1)+" and "+str(v2))
            
        #self.createClosedNeighbors()
        
        #self.stronglyChordalGraphDict = {0: [1, 2, 3, 4, 5], 1: [0, 2, 3, 4], 2: [0, 1, 4, 5], 3: [0, 1], 4: [0, 1, 2], 5: [0, 2]}
        
        #self.stronglyChordalGraphDict = {0: [5], 1: [4, 5, 6], 2: [3, 4], 3: [2, 4, 5], 4: [1, 2, 3, 5, 6], 5: [0, 1, 3, 4, 6], 6:[1, 4, 5]}
        
        #self.stronglyChordalGraphDict = { 0: [1, 2, 3, 4, 7],
                                          #1: [0, 2, 3, 4, 5],
                                          #2: [0, 1, 3, 5, 6, 4],
                                          #3: [0, 1, 2, 6, 7, 4],
                                          #4: [0, 1, 2, 3],
                                          #5: [1, 2],
                                          #6: [2, 3],
                                          #7: [0, 3]} #trampoline on n=4
        
        self.fromSCGToClosedNeighbors()
        
        self.recognitionAndSEO()
        
        print "==========================================="
        print "Recognition SEO: "+str(self.recognitionSEO,)
        
        self.fromSCGToClosedNeighbors()
        
        #self.recognitionSEO = [0, 1, 2, 3, 4, 5, 6] #a=0, b=1, c=2, d=3, e=4, f=5, g=6
        #self.recognitionSEO = [0, 1, 2, 3, 5, 6, 4] #a=0, b=1, c=2, d=3, e=4, f=5, g=6
        self.trampoSEO = copy.deepcopy(self.recognitionSEO)
        self.trampoSEO.reverse()
        
        strChordalEdges = 0
        for node, degree in self.stronglyChordalGraphDict.iteritems():
            strChordalEdges += len(degree) 
        
        self.addMoreEdges(self.noEdges - (strChordalEdges/2)) #adding more edges minus (trampoline + minimum scg edges)
        
        return True
    
    def addMoreEdges(self, requiredMoreEdges):
        """function to add more edges in the graph: moreEdges = givenEdges - treeEdges"""
        newEdges = 0
    
        #self.trampoSEO = [4, 6, 7, 0, 1, 2, 3, 5]
        #self.trampoSEO.reverse()
        #self.stronglyChordalGraphDict = {0: [1, 3, 4, 7, 2, 5], 
                                             #1: [0, 2, 4, 5, 3], 
                                             #2: [1, 3, 5, 6, 0], 
                                             #3: [2, 0, 6, 7, 1, 5], 
                                             #4: [0, 1], 
                                             #5: [1, 2, 0, 3], 
                                             #6: [2, 3], 7: [3, 0]}
    
        for i in range(len(self.trampoSEO)): 
            for j in range(len(self.trampoSEO)):
                if i < j and newEdges < requiredMoreEdges:
                    k = self.trampoSEO[i]
                    m = self.trampoSEO[j]
                    if not self.ifEdgeExist(self.stronglyChordalGraphDict, k, m):
                        self.addAnEdge(self.stronglyChordalGraphDict, k, m)
                        print "Added edge between: "+str(k)+" and "+str(m)
                        newEdges += 1
                        #self.plotSCG("Added edge between: "+str(k)+" and "+str(m))
                        #print self.stronglyChordalGraphDict
    
                        """for SCG recognition"""
                        #self.fromSCGToClosedNeighbors()
                        #if self.recognitionSEO:
                            #self.recognitionSEO = []
                        #self.recognitionAndSEO()
                        #print "==========================================="
                        #print "Recognition SEO: "+str(self.recognitionSEO,)
                        #self.fromSCGToClosedNeighbors()
                        """for SCG recognition"""
    
                        """for CG recognition"""
                        #self.fromClosedNeighborsToSCG()
                        #G = nx.Graph(self.stronglyChordalGraphDict)
                        #if nx.is_chordal(G):
                            #print "========================"
                            #print "This is a Chordal graph."
                            #print "========================"
                        """for CG recognition"""    
    
    def addAnEdge(self, graph, v1, v2):
        """function to add an edge in the graph"""
        graph[v1].append(v2)
        graph[v2].append(v1)
    
    def ifEdgeExist(self, graph, v1, v2):
        """function to check if edge exist"""
        if v2 in graph[v1] or v1 in graph[v2]:
            return True
        else:
            return False
        
    def fromSCGToClosedNeighbors(self):
        """function to create closed neighborhood from strong chordal graph"""
    
        self.closedNeighborhood = copy.deepcopy(self.stronglyChordalGraphDict)
    
        for vertex, neighbors in self.closedNeighborhood.iteritems():
            neighbors.append(vertex)
            self.closedNeighborhood.update({vertex: neighbors})
    
        print "\nClosed Neighborhood (Strongly Chordal Graph):-"
        print "=============================================="
        print self.closedNeighborhood
        
    def fromClosedNeighborsToSCG(self):
        """function to create strong chordal graph from closed neighborhood"""
        self.stronglyChordalGraphDict = copy.deepcopy(self.closedNeighborhood)
    
        for vertex, neighbors in self.stronglyChordalGraphDict.iteritems():
            if vertex in neighbors:
                neighbors.remove(vertex)    
        
    def plotCG(self):
        """function plot chordal graph (Trampoline)"""
        print "\n Printing Chordal Graph (Trampoline)(adjacency list): "
        print self.chordalGraph
        chordalEdges = 0
        for node, degree in self.chordalGraph.iteritems():
            chordalEdges += len(degree)
        print "\n No. of Chordal Graph Edges: "+ str(chordalEdges/2)
        CG = nx.Graph(self.chordalGraph) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(CG)
    
        plt.figure()
        plt.title("Chordal Graph")
        #plt.close('all')
        nx.draw_networkx(CG, pos, True)
        plt.show()
        
    def plotSCG(self, title):
        """function to plot strongly chordal graph"""
        print "\n Printing Strongly Chordal Graph (adjacency list): "
        print self.stronglyChordalGraphDict
        strChordalEdges = 0
        for node, degree in self.stronglyChordalGraphDict.iteritems():
            strChordalEdges += len(degree)
        print "\n No. of Strongly Chordal Tree Edges: "+ str(strChordalEdges/2)
        SCG = nx.Graph(self.stronglyChordalGraphDict) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(SCG)
    
        plt.figure()
        if not title:
            plt.title("Strongly Chordal Graph with "+str(self.noNodes)+" vertices and "+str(strChordalEdges/2)+" edges")
        else:
            plt.title(title)
        #plt.close('all')
        nx.draw_networkx(SCG, pos, True)
        plt.show(block=False)
        
    def createClosedNeighbors(self):
        """function to create closed neighborhood"""
        self.recognitionSEO = []
        self.stronglyChordalGraphDict2 = copy.deepcopy(self.stronglyChordalGraphDict)
        for vertex, neighbors in self.stronglyChordalGraphDict2.iteritems():
            neighbors.append(vertex)
            self.closedNeighborhood.update({vertex: list(set(neighbors))})
        
        #self.closedNeighborhood = {0: [0, 1, 2, 3, 4, 7], 1: [0, 1, 2, 3, 4, 5], 2: [0, 1, 2, 3, 5, 6], 
                                   #3: [0, 1, 2, 3, 6, 7], 4: [0, 1, 4], 5: [1, 2, 5], 6: [2, 3, 6], 
                                   #7: [0, 3, 7]} # not SCG
                                   
        #self.closedNeighborhood = {0: [0, 1, 2, 3, 4, 7], 1: [0, 1, 2, 3, 4, 5, 6], 2: [0, 1, 2, 3, 5, 6], 
                                   #3: [0, 1, 2, 3, 4, 6, 7], 4: [0, 1, 3, 4], 5: [1, 2, 5], 6: [1, 2, 3, 6], 
                                   #7: [0, 3, 7]} #SCG
        
        #self.closedNeighborhood = {1: [1, 2, 3, 4, 5, 6], 2: [1, 2, 3], 3: [1, 2, 3, 4, 5], 
                                   #4: [1, 3, 4, 5], 5: [1, 3, 4, 5, 6], 6: [1, 5, 6]} #SCG        
            
        print "\n Closed Neighborhood (Strongly Chordal Graph):-"
        print "=============================================="        
        print self.closedNeighborhood

        self.recognitionAndSEO()
        
        print "==========================================="
        print "Recognition SEO: "+str(self.recognitionSEO,)
    
    def updateClosedNeighbors(self, vertexToBeRemoved):
        """function to update closed neighborhood after removing a vertex 
        during the generation of a strong elimination ordering"""
        self.closedNeighborhood.pop(vertexToBeRemoved)
        
        for vertex, neighbors in self.closedNeighborhood.iteritems():
            if vertexToBeRemoved in neighbors:
                neighbors.remove(vertexToBeRemoved)     
    
    def recognitionAndSEO(self): #New implementation
        """function to recogize a strongly chordal graph and to produce a strong elimination ordering"""
        chainList = []
        if len(self.closedNeighborhood) > 1:
            for row, col in self.closedNeighborhood.iteritems():
                candidate = []
                tempOrderedNeighbors = []
                for c in col:
                    tempOrderedNeighbors.append(self.closedNeighborhood[c])
                
                tempOrderedNeighbors = sorted(tempOrderedNeighbors, key=lambda l: (len(l), l))
                
                for i in range(len(tempOrderedNeighbors)):
                    if i+1 < len(tempOrderedNeighbors):
                        v1 = tempOrderedNeighbors[i]
                        v2 = tempOrderedNeighbors[i+1]
                        if set(v1).issubset(set(v2)):
                            if v1 not in candidate:
                                v1Keys = [key  for (key, value) in self.closedNeighborhood.items() if value == v1]
                                for v1k in v1Keys:
                                    if v1k not in candidate:
                                        candidate.append(v1k)
                            if v2 not in candidate:
                                v2Keys = [key  for (key, value) in self.closedNeighborhood.items() if value == v2]
                                for v2k in v2Keys:
                                    if v2k not in candidate:
                                        candidate.append(v2k)
                        else:
                            candidate = []
                            break
                if candidate and candidate not in chainList:
                    chainList.append(candidate)
        elif len(self.closedNeighborhood) == 1:
            chainList.append(self.closedNeighborhood.keys())
        
        if chainList:
            chainList = sorted(chainList, key=lambda l: (len(l), l))
            #print(sorted(list2, key=lambda l: (len(l), l)))
            vertexToBeRemoved = chainList[0][0]
            print "\nChains: "+str(chainList,)+" and vertex to be removed "+str(vertexToBeRemoved)
            self.recognitionSEO.append(vertexToBeRemoved)
            
            if self.closedNeighborhood:
                self.updateClosedNeighbors(vertexToBeRemoved)
                self.recognitionAndSEO()