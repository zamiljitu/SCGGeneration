import random
import copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import lexBFS_V5 as LBFS #contains all the functions to get the Perfect Elimination Ordering

class StronglyChordalGraph:
    """This class turns a chordal graph into a strongly chordal graph. During this process it generates chordal graph for the given 
    number of vertices and and the number of edges. Then generate Perfect Elimination Ordering (PEO) and the neighborhood matrix of 
    the chordal graph and check for the patterns [1 1
                                                  1 0]."""
    def __init__(self, noNodes, noEdges):
        """initializes class variables"""
        self.noNodes = noNodes
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
 
    def createTree(self): 
        """function to create general tree"""        
        self.treeEdges = self.noNodes-1 #treeEdges = self.chordalTree-1
        
        for i in range(0, self.noNodes): 
            if not self.chordalTree:
                self.chordalTree[i] = list()
            elif i == 1:
                self.chordalTree[i-1].append(i)
                self.chordalTree[i] = list()
                self.chordalTree[i].append(i-1)
            else:
                methods = random.randint(1, 2)
                currentNodes = self.chordalTree.keys()
                if methods == 1:    # add a new node
                    v1 = random.choice(currentNodes)
                    self.addANode(v1, i) # i is the new node
                elif methods == 2:  # split an existing edge
                    while True:
                        v1 = random.choice(currentNodes)
                        if self.chordalTree[v1]:
                            v2 = random.choice(self.chordalTree[v1])
                            break               
                    self.splitAnEdge(v1, v2, i) # i is the new node
        
        rows = cols = len(self.chordalTree.keys())
        self.adj_matrix = self.adj_list_to_matrix(self.chordalTree, rows, cols)
    
        lexBFS = LBFS.lexBFS()
        neighborsDict, labelsList = lexBFS.neighbors(self.adj_matrix, rows, cols) #calling neighbors function from LBFS
    
        lexBFS.lexP(neighborsDict, labelsList, rows) #calling lexP function from LBFS
    
        self.peo = lexBFS.generatePEO() #calling peo function from LBFS
      
        return True

    def createCG(self):
        """function to create chordal graph"""
        self.addMoreEdges(self.noEdges - self.treeEdges) #adding more edges minus tree edges
    
        #self.chordalGraph = { 0: [0, 1, 2, 4, 5],
                              #1: [0, 1, 2],
                              #2: [0, 1, 2, 3, 4],  
                              #3: [2, 3, 4], 
                              #4: [0, 2, 3, 4, 5],
                              #5: [0, 4, 5]}
    
        #self.chordalGraph = { 0: [1, 2, 5], 
                              #1: [0, 2],
                              #2: [0, 1, 3, 4, 5],
                              #3: [2, 4, 5],
                              #4: [2, 3, 5],
                              #5: [0, 2, 3, 4]}
    
        #self.chordalGraph = { 0: [1, 2, 4, 5], 
                              #1: [0, 3, 4, 5],
                              #2: [0, 4],
                              #3: [1, 5],
                              #4: [0, 1, 2, 5],
                              #5: [0, 1, 3, 4]}
    
        #self.chordalGraph = { 0: [2, 3, 6], #this example used in the paper 
                              #1: [3, 4],
                              #2: [0, 3, 6],
                              #3: [0, 1, 2, 4, 6],
                              #4: [1, 3, 5, 6],
                              #5: [4, 6],
                              #6: [0, 2, 3, 4, 5]}
    
        #self.chordalGraph = { 0: [1, 2, 3, 6, 7], #this example used in the paper
                              #1: [0, 2, 3, 7],
                              #2: [0, 1, 3, 5, 6, 7],
                              #3: [0, 1, 2, 5, 7],
                              #4: [6, 7],
                              #5: [2, 3, 7],
                              #6: [0, 2, 4, 7],
                              #7: [0, 1, 2, 3, 4, 5, 6]}
                    
        #self.chordalGraph = { 0: [1], #this example used in the paper
                              #1: [0, 2, 3, 4],
                              #2: [1, 3, 4, 6],
                              #3: [1, 2, 4, 5, 6],
                              #4: [1, 2, 3, 5],
                              #5: [3, 4],
                              #6: [2, 3]}
        
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
        
        rows = cols = len(self.chordalGraph.keys())
        self.adj_matrix = self.adj_list_to_matrix(self.chordalGraph, rows, cols)
    
        lexBFS = LBFS.lexBFS()
        neighborsDict, labelsList = lexBFS.neighbors(self.adj_matrix, rows, cols) #calling neighbors function from LBFS
    
        lexBFS.lexP(neighborsDict, labelsList, rows) #calling lexP function from LBFS
    
        self.peo = lexBFS.generatePEO() #calling peo function from LBFS
    
        #self.createSCG()
        return True        
        
    def createSCG(self):
        """function to create strongly chordal graph"""
        
        if self.chordalGraph:
            rows = cols = len(self.chordalGraph.keys())
        else:
            self.chordalGraph = copy.deepcopy(self.chordalTree)
            rows = cols = len(self.chordalGraph.keys())
        
        print "Adjacency Matrix (Chordal Graph):-"
        print "================================="        
        self.display(self.adj_matrix, rows, cols)
        
        #self.adj_matrix = [[0, 1, 1, 0, 0, 0, 0],
                           #[1, 0, 1, 1, 0, 0, 0],
                           #[1, 1, 0, 1, 0, 1, 1],
                           #[0, 1, 1, 0, 1, 0, 1],
                           #[0, 0, 0, 1, 0, 0, 0],                           
                           #[0, 0, 1, 0, 0, 0, 1],
                           #[0, 0, 1, 1, 0, 1, 0]]
        
        self.neighborhoodMatrix = [[0 for y in range(cols)] for x in range(rows)]
        
        print "Perfect Elimination Ordering (Chordal Graph):-"
        print "============================================="
        for p in self.peo:
            print p,
            i = self.peo.index(p)
            self.peoLookupDict.update({i:p})
            self.neighborhoodMatrix[i][i] = 1
            for row, col in self.chordalGraph.iteritems():
                if p == row:
                    for c in col:
                        self.neighborhoodMatrix[i][self.peo.index(c)] = self.adj_matrix[p][c]
        
        print "\nNeighborhood Matrix (Chordal Graph):-"
        print "===================================="            
        self.display(self.neighborhoodMatrix, rows, cols)
        
        self.stronglyChordalGraphMat = copy.deepcopy(self.neighborhoodMatrix)
        self.DeltaFreeM(self.stronglyChordalGraphMat, rows, cols)
        
        return True

    def DeltaFreeM(self, M, rows, cols):
        """function to generate DeltaFreeM"""
        n = rows = cols
        
        #Make a list L of index pairs (i; j) in row-major order, such that i < j
        L = []
        for i in range(1, n):
            for j in range(1, n):
                if i < j:
                    tempL = []
                    tempL.append(i)
                    tempL.append(j)
                    L.append(tempL)
        
        #Search the upper left quadrant of M relative to (i, j)     
        for anL in L:
            startI = anL[0]
            startJ = anL[1]
            if M[startI][startJ] == 0:
                for i in range(startI, 0, -1):
                    for j in range(startJ, 0, -1):
                        if M[startI][j-1] == 1 and M[i-1][startJ] == 1 and M[i-1][j-1] == 1:
                            if M[startI][startJ] != 1:
                                print "Added an edge between: "+str(self.peoLookup(startI))+" and "+str(self.peoLookup(startJ))
                                M[startI][startJ] = 1 #M[i,j] = 1
                                M[startJ][startI] = 1 #M[j,i] = 1
                                break
        
        print "Neighborhood Matrix (Strongly Chordal Graph):-"
        print "=============================================="        
        self.display(M, rows, cols)
        
        self.convertMatToDict(M, rows, cols)
        self.createClosedNeighbors()
    
    def peoLookup(self, key):
        """function to retrieve original vertex name"""
        return self.peoLookupDict.get(key)
    
    def convertMatToDict(self, M, rows, cols):
        """function to create adjacency list from adjacency matrix"""
        for i in range(0, rows):
            for j in range(0, cols):
                if i == j:
                    M[i][j] = 0
                
        neighborsList = [[] for _ in xrange(rows)]
        neighborsDict = {}
        for i in xrange(rows):
            ii = self.peoLookup(i)
            for j in xrange(cols):
                if i != j and (M[i][j] != 0 and M[i][j] != 0. and M[i][j] != 0.0):
                    jj = self.peoLookup(j)
                    neighborsList[ii].append(jj)
            neighborsDict[ii] = neighborsList[ii]
        G = nx.Graph(neighborsDict)
        if not nx.is_chordal(G):
            #print "========================"
            #print "This is a Chordal graph."
            #print "========================"
        #else:
            for i in range(0, rows):
                for j in range(0, cols):
                    if i == j:
                        M[i][j] = 1
            self.createSCG()
        self.stronglyChordalGraphDict = copy.deepcopy(neighborsDict)
        
        self.scg_adj_matrix = self.adj_list_to_matrix(self.stronglyChordalGraphDict, rows, cols)
    
        print "Adjacency Matrix (Strongly Chordal Graph):-"
        print "==========================================="        
        self.display(self.scg_adj_matrix, rows, cols)
        
        #return neighborsDict
        
    def adj_list_to_matrix(self, adj_list, rows, cols):
        """function to create adjacency matrix from adjacency list"""
        adj_matrix = [[0 for y in range(cols)] for x in range(rows)]
        
        for row, col in adj_list.iteritems():
            for c in col:
                adj_matrix[row][c] = 1
        return adj_matrix
        
    def addANode(self, v1, v2):
        """function to add a node in the graph"""
        self.chordalTree[v1].append(v2)
        self.chordalTree[v2] = list()
        self.chordalTree[v2].append(v1)

    def splitAnEdge(self, v1, v2, v3):
        """function to split an edge"""
        self.chordalTree[v1].remove(v2)
        self.chordalTree[v1].append(v3)

        self.chordalTree[v2].remove(v1)
        self.chordalTree[v2].append(v3)

        self.chordalTree[v3] = list()
        self.chordalTree[v3].append(v1)
        self.chordalTree[v3].append(v2)
    
    def addAnEdge(self, graph, v1, v2):
        """function to add an edge in the graph"""
        graph[v1].append(v2)
        graph[v2].append(v1)
    
    def addMoreEdges(self, requiredMoreEdges):
        """function to add more edges in the graph: moreEdges = givenEdges - treeEdges"""
        newEdges = 0
        self.chordalGraph = copy.deepcopy(self.chordalTree)
        while newEdges < requiredMoreEdges:
            vertices = random.sample(self.chordalGraph, 2)
            u = vertices[0]
            v = vertices[1]
            if self.ifEdgeExist(self.chordalGraph, u, v):
                continue
            else:
                I_uv = list(set(self.chordalGraph[u]).intersection(self.chordalGraph[v]))
                if I_uv:
                    x = random.choice(I_uv)
                    auxNodes = list(set(self.chordalGraph[x]).difference(I_uv))
                    auxGraph = self.createAuxGraph(self.chordalGraph, auxNodes)
                    if not self.isReachable(auxGraph, u, v):
                        self.addAnEdge(self.chordalGraph, u, v)
                        #print "Add edge between: "+str(u)+" and "+str(v)
                        newEdges += 1
        print self.chordalGraph
        G = nx.Graph(self.chordalGraph)
        if nx.is_chordal(G):
            print "========================"
            print "This is a Chordal graph."
            print "========================"
            
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
    
    def display(self, mat, rows, cols):
        """function to format and display matrices"""
        if type(mat) is list:
            for i in xrange(rows):
                for j in xrange(cols):
                    print '{:5}'.format(mat[i][j]), #formatting the display of a matrix
                print
        else:
            for i in xrange(rows):
                for j in xrange(cols):
                    print '{:5}'.format(mat[i,j]), #formatting the display of a matrix
                print 
    
    def plotTree(self):
        """function plot (chordal) tree"""
        print "Printing (Chordal) Tree (adjacency list): "
        print self.chordalTree
        chordalEdges = 0
        for node, degree in self.chordalTree.iteritems():
            chordalEdges += len(degree)
        print "No. of (Chordal) Tree Edges: "+ str(chordalEdges/2)
        tree = nx.Graph(self.chordalTree) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(tree)
    
        plt.figure()
        #plt.title("(Chordal) Tree, PEO: "+str(self.peo))
        plt.title("(Chordal) Tree")
        #plt.close('all')
        nx.draw_networkx(tree, pos, True)
        plt.show()
        
    def plotCG(self):
        """function plot chordal graph"""
        print "Printing Chordal Graph (adjacency list): "
        print self.chordalGraph
        chordalEdges = 0
        for node, degree in self.chordalGraph.iteritems():
            chordalEdges += len(degree)
        print "No. of Chordal Graph Edges: "+ str(chordalEdges/2)
        CG = nx.Graph(self.chordalGraph) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(CG)
    
        plt.figure()
        #plt.title("Chordal Graph, PEO: "+str(self.peo))
        plt.title("Chordal Graph")
        #plt.close('all')
        nx.draw_networkx(CG, pos, True)
        plt.show()
        
    def plotSCG(self):
        """function plot strongly chordal graph"""
        print "Printing Strongly Chordal Graph (adjacency list): "
        print self.stronglyChordalGraphDict
        strChordalEdges = 0
        for node, degree in self.stronglyChordalGraphDict.iteritems():
            strChordalEdges += len(degree)
        print "No. of Strongly Chordal Tree Edges: "+ str(strChordalEdges/2)
        SCG = nx.Graph(self.stronglyChordalGraphDict) #converting "dictionary typed graph" to "networkx graph"
        pos = nx.spring_layout(SCG)
    
        plt.figure()
        #plt.title("Strongly Chordal Graph, SEO: "+str(self.peo))
        plt.title("Strongly Chordal Graph with "+str(self.noNodes)+" vertices and "+str(strChordalEdges/2)+" edges")
        #plt.close('all')
        nx.draw_networkx(SCG, pos, True)
        plt.show()
        
    def createClosedNeighbors(self):
        self.recognitionSEO = []
        self.stronglyChordalGraphDict2 = copy.deepcopy(self.stronglyChordalGraphDict)
        for vertex, neighbors in self.stronglyChordalGraphDict2.iteritems():
            neighbors.append(vertex)
            self.closedNeighborhood.update({vertex: neighbors})
        
        print "Closed Neighborhood (Strongly Chordal Graph):-"
        print "=============================================="        
        print self.closedNeighborhood
        
        self.recognitionAndSEO()
        
        print "==========================================="
        print "Recognition SEO: "+str(self.recognitionSEO,)
        #print "Recognition SEO: "+str(self.peo)
    
    def updateClosedNeighbors(self, vertexToBeRemoved):
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
            print "Chains: "+str(chainList,)+" and vertex to be removed "+str(vertexToBeRemoved)
            self.recognitionSEO.append(vertexToBeRemoved)
            
            if self.closedNeighborhood:
                self.updateClosedNeighbors(vertexToBeRemoved)
                self.recognitionAndSEO()
            