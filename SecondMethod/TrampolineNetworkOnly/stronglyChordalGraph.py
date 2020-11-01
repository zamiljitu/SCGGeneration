import random
import numpy as np

import itertools
import copy

import networkx as nx
import matplotlib.pyplot as plt

class StronglyChordalGraph:
    """This class turns the trampoline into strongly chordal graph. During this process it generates a trampoline for the given 
    number of vertices and and the number of edges. Then generate strongly chordal graph."""
    
    def __init__(self, nodesList, noEdges):
        self.nodesList = nodesList
        self.noNodes = 0
        self.noEdges = noEdges
        self.treeEdges = 0
        self.chordalTree = {}
        self.trampolines = {}
        self.trampolinesConnected = {}
        self.stronglyChordalGraphDict = {}
        self.closedNeighborhood = {}
        self.recognitionSEO = []
        self.trampoAllNodes = []
        self.trampoCompNodes = []
        self.trampoIndNodes = []

    def createTrampolines(self):
        """function to create trampolines"""
        
        start = 0
        
        for i in range(len(self.nodesList)):
            noNodes = int(self.nodesList[i])

            stop = start + noNodes
            allNodes = range(start, stop)
            start = stop
            
            self.noNodes += len(allNodes)
                                    
            compNodes = allNodes[:len(allNodes)//2]
            indNodes = allNodes[len(allNodes)//2:]
            
            self.trampoAllNodes.append(allNodes)
            self.trampoCompNodes.append(compNodes)
            self.trampoIndNodes.append(indNodes)
            
            cycleEdges = []
            
            for j, k in zip(compNodes, compNodes[1:] + compNodes[:1]):
            #for i in compNodes:
                #j = i % len(compNodes)
                #k = (i+1) % len(compNodes)
                e = []
                e.append(j)
                e.append(k)
                cycleEdges.append(e)
                if not self.trampolines:
                    self.trampolines[j] = list()
                    self.trampolines[j].append(k)
                    self.trampolines[k] = list()
                    self.trampolines[k].append(j)
                else:
                    if j not in self.trampolines:
                        self.trampolines[j] = list()
                    self.trampolines[j].append(k)
                    if k not in self.trampolines:
                        self.trampolines[k] = list()
                    self.trampolines[k].append(j)
            
            #cycleNodes, cycleEdges = self.createEdgeList(self.trampolines)
            
            for ce in range(len(cycleEdges)):
                for i in range(len(indNodes)):
                    if ce == i:
                        for c in cycleEdges[ce]:
                            self.trampolines[c].append(indNodes[i])
                            if indNodes[i] not in self.trampolines:
                                self.trampolines[indNodes[i]] = list()
                            self.trampolines[indNodes[i]].append(c)
            
            allNodes, cyclePlusIndEdges = self.createEdgeList(self.trampolines)
            
            self.createCompleteGraph(compNodes, cyclePlusIndEdges, self.trampolines)
            
            self.plotGraph(self.trampolines, "Trampolines")
    
        self.createConnTrampolines()
        return True        
    
    def createConnTrampolines(self):
        """function to create connected trampolines"""
        
        newEdges = 0
        self.trampolinesConnected = copy.deepcopy(self.trampolines)
        
        connComp = len(list(sorted(nx.connected_components(nx.Graph(self.trampolinesConnected)))))
        while connComp > 1:
            j = newEdges % len(self.nodesList)
            k = (newEdges+1) % len(self.nodesList)
            u = random.choice(self.trampoAllNodes[j])
            v = random.choice(self.trampoAllNodes[k])
            self.addAnEdge(self.trampolinesConnected, u, v)
            print "Added edge between: "+str(u)+" and "+str(v)
            newEdges += 1
            self.plotGraph(self.trampolinesConnected, "Connected Trampolines")
            connComp = len(list(sorted(nx.connected_components(nx.Graph(self.trampolinesConnected)))))
            
            print self.trampolinesConnected
            G = nx.Graph(self.trampolinesConnected)
            if not nx.is_chordal(G):
                print "============================"
                print "This is NOT a Chordal graph."
                print "============================"
         
        #self.addMoreEdges(self.noEdges)
    
    def addMoreEdges(self, requiredMoreEdges):
        """function to create connected trampolines"""
        newEdges = 0
        
        while newEdges < requiredMoreEdges:
            trampolines = random.sample(range(len(self.trampoAllNodes)),2)
            u = random.choice(self.trampoAllNodes[trampolines[0]])
            v = random.choice(self.trampoAllNodes[trampolines[1]])
            if self.ifEdgeExist(self.trampolinesConnected, u, v):
                continue
            else:
                I_uv = list(set(self.trampolinesConnected[u]).intersection(self.trampolinesConnected[v]))
                if I_uv:
                    x = random.choice(I_uv)
                    auxNodes = list(set(self.trampolinesConnected[x]).difference(I_uv))
                    auxGraph = self.createAuxGraph(self.trampolinesConnected, auxNodes)
                    if not self.isReachable(auxGraph, u, v):
                        self.addAnEdge(self.trampolinesConnected, u, v)
                        print "Added edge between: "+str(u)+" and "+str(v)
                        newEdges += 1
                        self.plotGraph(self.trampolinesConnected, "Connected Trampolines")
                
                        print self.trampolinesConnected
                        G = nx.Graph(self.trampolinesConnected)
                        if not nx.is_chordal(G):
                            print "============================"
                            print "This is NOT a Chordal graph."
                            print "============================"
        print str(newEdges)+" edges added to connect trampolines"
        
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
        """function to create strongly chordal graph"""
        self.stronglyChordalGraphDict = copy.deepcopy(self.trampolinesConnected)
        
        for i in range(len(self.nodesList)):
            alreadyChosen = []
            v1 = random.choice(list(set(self.trampoIndNodes[i]).difference(set(alreadyChosen))))
            alreadyChosen.append(v1)
            neighborsOfV1 = self.stronglyChordalGraphDict.get(v1)
            notNeighborsOfV1 = list(set(self.trampoCompNodes[i]).difference(set(neighborsOfV1)))
            for v2 in notNeighborsOfV1:
                self.addAnEdge(self.stronglyChordalGraphDict, v1, v2)
                print "\nAdded edge between: "+str(v1)+" and "+str(v2)
                
                G = nx.Graph(self.stronglyChordalGraphDict)
                if not nx.is_chordal(G):
                    print "============================"
                    print "This is NOT a Chordal graph."
                    print "============================"
                    
        self.createClosedNeighbors()
        
        return True
    
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
        
    def isReachable(self, auxGraph, v1, v2):
        """function (BFS) to check path between v1 and v2"""
        visited =[False]*(self.noNodes)
        queue=[]
        queue.append(v1)
        visited[v1] = True
  
        while queue:
            n = queue.pop(0)
            if n == v2:
                return True
            for i in auxGraph[n]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        return False
                
    def createAuxGraph(self, graph, auxNodes):
        """function to creae graphs C and G[C]"""
        auxGraph = {}
        for i in auxNodes:
            if graph.has_key(i):
                auxGraph[i] = list(set(graph[i]).intersection(set(auxNodes)))
        return auxGraph
    
    def plotGraph(self, graphToDraw, graphName):
        """function plot chordal graph"""
        
        edges = 0
        for node, degree in graphToDraw.iteritems():
            edges += len(degree)           
        
        GD = nx.Graph(graphToDraw)
        pos = nx.spring_layout(GD)
        
        plt.figure()
        if graphName == 1:
            print "\Trampolines (connected): "+str(self.trampolinesConnected)
            print "\nNo. of edges in the Trampolines (connected) : "+ str(edges/2)
            plt.title("Trampolines (connected)")
        elif graphName == 2:
            print "\nStrongly Chordal Graph: "+str(self.stronglyChordalGraphDict)
            print "\nNo. of edges in the Strongly Chordal Graph: "+ str(edges/2)
            plt.title("Strongly Chordal Graph")
        else:
            print "\nNo. of edges in the "+ graphName+ ": "+ str(edges/2)
            plt.title(graphName)
            
        nx.draw_networkx(GD, pos, True)
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
            
        print "\n Closed Neighborhood (Strongly Chordal Graph):-"
        print "=============================================="        
        print self.closedNeighborhood

        self.recognitionAndSEO()
        
        print "==========================================="
        print "Recognition SEO ("+str(len(self.recognitionSEO))+"): "+str(self.recognitionSEO,)
    
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