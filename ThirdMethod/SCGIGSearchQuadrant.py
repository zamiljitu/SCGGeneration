class SCGIGSearchQuadrant:
    """This class Search quadrants for a Delta submatrix in a strongly chordal graph"""
    
    def __init__(self, ii, jj, TVIMatrix):
        self.ii = ii
        self.jj = jj
        self.X = TVIMatrix
        
    def searchInM(self):
        """function to search 1 1 
                              0 1 in the totally balanced matrix (neighborhood matrix)"""
        for j in range(self.jj, len(self.X)-1, 1): #downright (4th quadrant)
            for i in range(self.ii, len(self.X)-1, 1):
                if self.X[self.ii][j+1] == 1 and self.X[i+1][j+1] == 1 and self.X[i+1][self.jj] == 0:
                    return True
                
        for j in range(self.jj, 0, -1): #downleft (3rd quadrant)
            """function to search 1 1 
                                  0 1 in the totally balanced matrix (neighborhood matrix)"""
            for i in range(self.ii, len(self.X)-1, 1):
                if self.X[self.ii][j-1] == 1 and self.X[i+1][j-1] == 0 and self.X[i+1][self.jj] == 1:
                    return True
                
        for j in range(self.jj, 0, -1): #upleft (2nd quadrant)
            """function to search 1 1 
                                  0 1 in the totally balanced matrix (neighborhood matrix)"""            
            for i in range(self.ii, 0, -1):
                if self.X[self.ii][j-1] == 0 and self.X[i-1][j-1] == 1 and self.X[i-1][self.jj] == 1:
                    return True