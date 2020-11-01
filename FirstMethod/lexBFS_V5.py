from operator import itemgetter
import numpy as np

class lexBFS:
    """This class implements lexicographic breadth first search (BFS)."""
    
    def __init__(self):
        self.orderedQueue = []
        self.numberedVertices = []
        self.alphaDict = {}
        self.alphaLabelsDict = {}
        self.peo = []
    
    def alphaLookup(self, key):
        """function to retrieve original vertex name"""
        return alphaDict.get(key)
    
    def neighbors(self, M, rows, cols):
        """function to create neighborslist of each vertex"""
        labelsList = [[] for _ in xrange(rows)]
        neighborsList = [[] for _ in xrange(rows)]
        neighborsDict = {}
        for i in xrange(rows):
            for j in xrange(cols):
                #print type(M[i][j])
                if i != j and (M[i][j] != 0 and M[i][j] != 0. and M[i][j] != 0.0):
                    neighborsList[i].append(j)
            neighborsDict[i] = neighborsList[i]
        return neighborsDict, labelsList
    
    def lexP(self, neighborsDict, labelsList, rows):
        """function to create lexicographic perfect ordering. See the following paper (Section 4.2. Perfect orderings.):
        ALGORITHMIC ASPECTS OF VERTEX ELIMINATION ON GRAPHS* by DONALD J. ROSE, R. ENDRE TARJAN AND GEORGE S. LUEKER"""        
        for i in range(rows, 0, -1): # for i:= n step-1 until 1 do begin
            if i == rows:
                v = i-1 #select: pick an unnumbered vertex v with largest label; (TO PICK FIRST VERTEX ONLY)
                global alphaDict
                alphaDict = {}
                numberedVertices = []
                self.orderedQueue.append(v)
            else:
                v = self.pickVertex(labelsList, rows, i) #select: pick an unnumbered vertex v with largest label;
                
            alphaDict[i] = v #comment assign v the number i, \alpha(i):= v;
            numberedVertices.append(v)
            self.orderedQueue.remove(v)
            for key, value in neighborsDict.iteritems():
                if v == key:
                    for val in value:
                        if val not in numberedVertices:
                            labelsList[val].append(i) #update2: for each unnumbered vertex $w\in adj (v)$ io add to label(w);
                            if val not in self.orderedQueue:
                                self.orderedQueue.append(val)
        
    def generatePEO(self):
        """function to generate Perfect Elimination Ordering (PEO)"""
        for key, value in sorted(alphaDict.iteritems(), key=lambda x:x[0]): # key, value
            self.peo.append(value)
        return self.peo
    
    def generateEdgePairs(self, labelsList, rows):
        """function to generate edge from pair of vertices"""        
        for index, elem in enumerate(labelsList):
            k = next(key for key, value in alphaDict.iteritems() if value == index)
            self.alphaLabelsDict.update({k:elem})
            
        edgePairs = {}
        for i in range(rows, 0, -1):
            pairs = []
            for key, value in self.alphaLabelsDict.iteritems():
            #for key, value in sorted(self.alphaLabelsDict.iteritems(), key=lambda x:x[0], reverse=True): # key, value
                if value and i > key and i not in value:
                        pairs.append(key)
            if pairs:
                edgePairs.update({i: pairs[::-1]})    
        return edgePairs

    def pickVertex(self, labelsList, rows, i):
        """function to pick an unnumbered vertex v with largest label"""        
        tempList = []
        tempLabelsList = [[] for _ in xrange(len(labelsList))]
        for i in range(len(self.orderedQueue)):
            tempList.append(labelsList[self.orderedQueue[i]])
            tempLabelsList[self.orderedQueue[i]] = labelsList[self.orderedQueue[i]]
        tempList.sort(reverse=True)
        v = [i for i,x in enumerate(tempLabelsList) if x == tempList[0]]
        return v[-1]