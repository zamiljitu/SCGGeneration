import random
import copy
import itertools
import numpy as np
import networkx as nx 
import matplotlib.pyplot as plt
from operator import itemgetter

import SCGIGSearchQuadrant as SCGIGSQ

class StronglyChordalGraph:
    """This class turns the chordal gaph into strongly chordal graph. During this process it generates a Delta-free submatrix for the 
    given number of vertices. Then generate a strongly chordal graph."""
    
    def __init__(self, noVertices):
        """initializes class variables"""
        self.noRows = noVertices
        self.noCols = noVertices
        self.stronglyChordalGraphDict = {}
        self.closedNeighborhood = {}
        self.recognitionSEO = []
        self.recognitionSEOOriginal = []
        self.M = []
        self.subTreesList = []
        self.runOfOnesAll = []
        
    def createDeltaFreeMatrix(self):
        """function to create Delta-free matrix M"""
        
        MCreated = False
        self.M = [[0 for y in range(self.noCols)] for x in range(self.noRows)]

        #for i in range(0, self.noRows):
        for j in range(self.noCols-1, -1, -1):
            lowerAntiDiagonals = self.noCols-j-1
            if lowerAntiDiagonals == 0:
                randLength = 0
                runOfZeros = [0] * (self.noCols-1)
                runOfOnes = [1] * (randLength+1)
                runOfOnes = runOfZeros+runOfOnes
            else:
                randLength = random.randint(0, lowerAntiDiagonals)
                runOfZerosBefore = [0] * j
                runOfOnes = [1] * (randLength+1)
                runOfZerosAfter = [0] * (self.noCols-j-randLength-1)
                #if randLength < lowerAntiDiagonals:
                    #runOfZerosAfter = [0] * (lowerAntiDiagonals-randLength)
                runOfOnes = runOfZerosBefore+runOfOnes+runOfZerosAfter
            self.runOfOnesAll.append(runOfOnes)
                
            print randLength
            #randLength.append(random.randint(0, self.noCols-lowerAntiDiagonals))
        
        self.createSubTrees()
    
        MCreated = True
        return MCreated
    
    def createSubTrees(self):
        """function to create subtrees from M"""
        self.subTreesList = []
        for i in range(0, self.noRows):
            subTree = []
            for j in range(0, self.noCols):
                self.M[i][j] = self.runOfOnesAll[i][j]
                if self.runOfOnesAll[i][j] == 1:
                    subTree.append(j)
                    
            self.subTreesList.append(subTree)
            print self.subTreesList
                        
        print "\nDelta-free Matrix M:-"
        print "================================================"
        self.display(self.M, self.noRows, self.noCols)

    def display(self, mat, rows, cols):
        """function to format and display matrices"""
        
        if type(mat) is list:
            for i in range(rows):
                for j in range(cols):
                    print '{:3}'.format(mat[i][j]), #formatting the display of a matrix
                print
        else:
            for i in range(rows):
                for j in range(cols):
                    print '{:3}'.format(mat[i,j]), #formatting the display of a matrix
                print
    
    def createSCG(self):
        """function to create strongly chordal graph from a Delta-free Matrix (subtrees)"""
        
        SCGCreated = False
        #self.subTreesList = [[5], [4], [3,4,5], [2,3,4,5],[1,2],[0,1,2,3,4]]
        #self.subTreesList = [[3], [2], [1,2,3], [0,1,2,3]]
        #self.subTreesList = [[7], [6], [5], [4,5], [3,4], [2,3,4,7], [1,2,3,4,6,7], [0,1,2,3,4,5,6]]
        for i in range(len(self.subTreesList)):
            for j in range(i+1, len(self.subTreesList)):
                weight = list(set(self.subTreesList[i]).intersection(set(self.subTreesList[j])))
                if len(weight) >= 1:
                    if i in self.stronglyChordalGraphDict:
                        self.stronglyChordalGraphDict[i].append(j)
                    else:
                        self.stronglyChordalGraphDict[i] = list()
                        self.stronglyChordalGraphDict[i].append(j)
                    if j in self.stronglyChordalGraphDict:
                        self.stronglyChordalGraphDict[j].append(i)
                    else:
                        self.stronglyChordalGraphDict[j] = list()
                        self.stronglyChordalGraphDict[j].append(i)
                else:
                    if i not in self.stronglyChordalGraphDict:
                        self.stronglyChordalGraphDict[i] = list()
                    if j not in self.stronglyChordalGraphDict:
                        self.stronglyChordalGraphDict[j] = list()
        
        self.stronglyChordalGraphDict = nx.Graph(self.stronglyChordalGraphDict)
        connComp = sorted(nx.connected_components(self.stronglyChordalGraphDict))
        self.stronglyChordalGraphDict = nx.to_dict_of_lists(self.stronglyChordalGraphDict)
        
        for cc in sorted(connComp, key = len, reverse=True):
            tempSCGDict = {x:self.stronglyChordalGraphDict[x] for x in cc}

            self.fromSCGToClosedNeighbors(1, tempSCGDict)
        
            self.fromSCGToClosedNeighbors(999, tempSCGDict) #just any number other than 1
        
            self.recognitionSEOOriginal += self.recognitionSEO
        
        SCGCreated = True
        return SCGCreated
    
    def turnZeroToOne(self, i, j):
        """function to turn ZERO to ONE"""
        isTurned = False
        notTurningReason = 0
        
        if i < self.noRows and j < self.noCols:
            if self.M[i][j] != 1:
                self.SCGInsertion = SCGIGSQ.SCGIGSearchQuadrant(i, j, self.M)
                if not self.SCGInsertion.searchInM(): #and not self.SCGInsertion.insertQueryTransposedSCG():
                    #self.M[i][j] = 1
                    self.runOfOnesAll[i][j] = 1
                    isTurned = True
                    #print "\nDelta-free Matrix M (after turning ZERO in ["+str(i)+","+str(j)+"] to ONE)"
                    #print "================================================"
                    #self.display(self.M, self.noRows, self.noCols)
                else:
                    notTurningReason = 3
            else:
                notTurningReason = 2
        else:
            notTurningReason = 1        
        
        if isTurned:
            self.createSubTrees()
            self.createSCG()
            self.plotGraph()
            #self.fromSCGToClosedNeighbors(1, self.stronglyChordalGraphDict)
        
            #self.fromSCGToClosedNeighbors(999, self.stronglyChordalGraphDict) #just any number other than 1
            
        return isTurned, notTurningReason
                
    def fromSCGToClosedNeighbors(self, time, tempSCGDict):
        """function to create closed neighborhood from strong chordal graph"""
        
        #self.closedNeighborhood = copy.deepcopy(self.stronglyChordalGraphDict)
        self.closedNeighborhood = copy.deepcopy(tempSCGDict)
        
        for vertex, neighbors in self.closedNeighborhood.iteritems():
            neighbors.append(vertex)
            self.closedNeighborhood.update({vertex: neighbors})
        
        if time == 1: #just for implementation purpose
            print "\nClosed Neighborhood (Strongly Chordal Graph):-"
            print "=============================================="
            print self.closedNeighborhood
            
            self.recognitionSEO = [] ###
            self.recognitionAndSEO()
            
            print "\nRecognition SEO:-"
            print "================="
            print self.recognitionSEO,
            print "\n"
        
    def updateClosedNeighbors(self, vertexToBeRemoved):
        """function to update closed neighborhood after deleting a (simple) vertex"""
        
        self.closedNeighborhood.pop(vertexToBeRemoved)
        
        for vertex, neighbors in self.closedNeighborhood.iteritems():
            if vertexToBeRemoved in neighbors:
                neighbors.remove(vertexToBeRemoved)
        
    def recognitionAndSEO(self): #New implementation
        """function to recogize a strongly chordal graph and to produce a strong elimination ordering"""
        
        chainList = []
        recogSEO = []
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

    def plotGraph(self):
        """function to plot strongly chordal graph"""
        
        print "\nStrongly Chordal Graph (adjacency list): "
        print self.stronglyChordalGraphDict
        edgesCount = 0
        verticesCount = 0
        for vertices, degree in self.stronglyChordalGraphDict.iteritems():
            verticesCount += 1
            edgesCount += len(degree)
        print "\nNo. of Strongly Chordal Graph Vertices: "+ str(verticesCount)
        print "\nNo. of Strongly Chordal Graph Edges: "+ str(edgesCount/2)
        
        SCG = nx.Graph(self.stronglyChordalGraphDict) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(SCG)
        
        plt.figure()
        plt.title("Strongly Chordal Graph with "+str(verticesCount)+" vertices and "+str(edgesCount/2)+" edges")

        nx.draw_networkx(SCG, pos, True)
        
        plt.show(block=False)