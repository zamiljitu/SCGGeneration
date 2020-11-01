import Tkinter
import tkMessageBox

import random

import stronglyChordalGraphIG as SCG

def isStrInt(str):
    try: 
        int(str)
        return True
    except ValueError:
        return False
    
class gui_tk(Tkinter.Tk):
    """This is the main class contains mainly gui_tk"""
    
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.SCGGeneration = SCG.StronglyChordalGraph(0)
        self.Matrix = False
        self.SCG = False
        
    def initialize(self):
        """function to initialize the components in the gui"""
        
        self.grid()
        
        self.lblNumVerticesText = Tkinter.StringVar()
        lblNumVertices = Tkinter.Label(self, textvariable=self.lblNumVerticesText)
        lblNumVertices.grid(row=0, column=0, sticky=Tkinter.W)
        self.lblNumVerticesText.set(u'No. of vertices')
    
        self.verticesEntry = Tkinter.Entry(self)
        self.verticesEntry.grid (row=0, column=1, sticky=Tkinter.W)
        
        buttonCreateTVIM = Tkinter.Button(self,text=u'Generate Tree-vertex Incidence Matrix', 
                                             command=self.onCreateMatrixClick)
        buttonCreateTVIM.grid(row=1, column=0, sticky=Tkinter.W)
        
        buttonViewSCG = Tkinter.Button(self,text=u'Generate Strongly Chordal Graph', 
                                           command=self.onCreateSCGClick)
        buttonViewSCG.grid(row=2, column=0, sticky=Tkinter.W)
        
        buttonViewSCG = Tkinter.Button(self,text=u'View Strongly Chordal Graph', 
                                           command=self.onViewSCGClick)
        buttonViewSCG.grid(row=2, column=1, sticky=Tkinter.W)
        
        self.lblNumVerticesText = Tkinter.StringVar()
        lblNumVertices = Tkinter.Label(self, textvariable=self.lblNumVerticesText)
        lblNumVertices.grid(row=3, column=0, sticky=Tkinter.W)
        self.lblNumVerticesText.set(u'Choose a zero (zero-based indexing (i,j))')
        
        self.chosenEdgeEntry = Tkinter.Entry(self)
        self.chosenEdgeEntry.grid (row=3, column=1, sticky=Tkinter.W)
        
        buttonCreateTZTO = Tkinter.Button(self,text=u'Turn ZERO to ONE', 
                                              command=self.onTurnZeroToOneClick)
        buttonCreateTZTO.grid(row=4, column=1, sticky=Tkinter.W)        
        
    def onCreateMatrixClick(self):
        """function to check valid input and call create and display matrix"""
        
        noVertices = self.verticesEntry.get()
        if isStrInt(noVertices):
            noVertices = int (self.verticesEntry.get())
            if (noVertices < 0):
                tkMessageBox.showwarning("Warning","Entry for vertices is less than 0.")
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for vertices is not an integer.")
            return
        
        self.SCGGeneration = SCG.StronglyChordalGraph(noVertices)
        self.Matrix = self.SCGGeneration.createDeltaFreeMatrix()
        
    def onCreateSCGClick(self):
        """function to call create strongly chordal graph"""
        
        if self.Matrix:
            self.SCG = self.SCGGeneration.createSCG()  

    def onViewSCGClick(self):
        """function to call plot strongly chordal graph"""
            
        if self.SCG:
            self.SCGGeneration.plotGraph()
        else:
            tkMessageBox.showwarning("Warning","Create Strongly Chordal Graph first to view Strongly Chordal Graph.")
            return
        
    def onTurnZeroToOneClick(self):
        """function to turn ZERO to ONE in a tree-vertex incidence matrix"""
        
        chosenEdge = self.chosenEdgeEntry.get()
        if len(self.chosenEdgeEntry.get())==0:
            tkMessageBox.showwarning("Warning","Cannot be empty. Enter a valid index to turn a ZERO to ONE.")
            return            
        chosenEdge = chosenEdge.strip()
        nodes = chosenEdge.split(",")
        if len(nodes)>2:
            tkMessageBox.showwarning("Warning","Enter a valid index to turn a ZERO to ONE.")
            return
        
        if int(nodes[1]) <= int(self.verticesEntry.get())-int(nodes[0])-1:
            tkMessageBox.showwarning("Warning","Enter a valid index in the lower antidiagonal matrix.")
            return
        
        if self.Matrix:
            u = int(nodes[0])
            v = int(nodes[1])
            isTurned, notTurningReason = self.SCGGeneration.turnZeroToOne(u, v)
            if not isTurned:
                if notTurningReason == 1:
                    tkMessageBox.showwarning("Warning", " Either i or j is out of the index. Enter a valid index.")
                    return                
                elif notTurningReason == 2:
                    tkMessageBox.showwarning("Warning", "M ["+ chosenEdge + "] is already 1.")
                    return
                elif notTurningReason == 3:
                    tkMessageBox.showwarning("Warning", "The changing of ZERO in ["+ chosenEdge + "] to ONE will generate Delta-free matrix.")
                    return
        else:
            tkMessageBox.showwarning("Warning","Create Strongly Chordal Graph first to delete an edge.")
            return
        
def center(toplevel):
    """function to compute the center of the screen and place the window in the center"""
    
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

if __name__ == "__main__":
    """main function which is the starting point of this strongly chordal graph generation technique"""
    
    app = gui_tk(None)
    app.title("Strongly Chordal Graph (SCG) Generation")
    app.geometry('380x125')#window size
    center(app)
    app.mainloop()
    app.quit()