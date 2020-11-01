import Tkinter
import tkMessageBox

import random

import stronglyChordalGraph as SCG

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
        self.tree = SCG.StronglyChordalGraph(0, 0)
        self.Tree = False
        self.CG = False
        self.SCG = False
        
    def initialize(self):
        """initializing GUI controls"""
        self.grid()

        self.lblNumNodesText = Tkinter.StringVar()
        lblNodes = Tkinter.Label(self, textvariable=self.lblNumNodesText)
        lblNodes.grid(row=0, column=0, sticky=Tkinter.W)
        self.lblNumNodesText.set(u'No. of Nodes ')

        self.nodesEntry = Tkinter.Entry(self)
        self.nodesEntry.grid (row=0, column=1, sticky=Tkinter.W)
        
        self.lblNumEdgesText = Tkinter.StringVar()
        lblEdges = Tkinter.Label(self, textvariable=self.lblNumEdgesText)
        lblEdges.grid(row=1, column=0, sticky=Tkinter.W)
        self.lblNumEdgesText.set(u'No. of Edges ')
    
        self.edgesEntry = Tkinter.Entry(self)
        self.edgesEntry.grid (row=1, column=1, sticky=Tkinter.W)
        
        buttonCreateTree = Tkinter.Button(self,text=u'Generate Tree', 
                                            command=self.onCreateTreeClick)
        buttonCreateTree.grid(row=2, column=0, sticky=Tkinter.W)      
    
        buttonViewCG = Tkinter.Button(self,text=u'View (Chordal) Tree', 
                                          command=self.onViewTreeClick)
        buttonViewCG.grid(row=2, column=1, sticky=Tkinter.W)        
        
        buttonCreateCG = Tkinter.Button(self,text=u'Generate Chordal Graph', 
                                              command=self.onCreateCGClick)
        buttonCreateCG.grid(row=3, column=0, sticky=Tkinter.W)      
        
        buttonViewCG = Tkinter.Button(self,text=u'View Chordal Graph', 
                                              command=self.onViewCGClick)
        buttonViewCG.grid(row=3, column=1, sticky=Tkinter.W)
        
        buttonCreateSCG = Tkinter.Button(self,text=u'Generate Strongly Chordal Graph', 
                                              command=self.onCreateSCGClick)
        buttonCreateSCG.grid(row=4, column=0, sticky=Tkinter.W)          
        
        buttonViewSCG = Tkinter.Button(self,text=u'View Strongly Chordal Graph', 
                                              command=self.onViewSCGClick)
        buttonViewSCG.grid(row=4, column=1, sticky=Tkinter.W)
    
    #def text_changed(*args):
        #print self.nodesEntry.get()
            
    def onCreateTreeClick(self):
        """function to check valid input and create an instance of StronglyChordalGraph class"""

        noNodes = self.nodesEntry.get()
        if isStrInt(noNodes):
            noNodes = int (self.nodesEntry.get())
            if (noNodes < 0):
                tkMessageBox.showwarning("Warning","Entry for nodes is less than 0.")
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for nodes is not an integer.")
            return
        
        noEdges = self.edgesEntry.get()
        if isStrInt(noEdges):
            noEdges = int (self.edgesEntry.get())
            if (noEdges < 0):
                tkMessageBox.showwarning("Warning","Entry for edges is less than 0.")
                return
            if (noEdges < (noNodes-1)):
                tkMessageBox.showwarning("Warning","Entry for edges must be enough for a tree structure. Needs %d." %(noNodes-1))
                return
            if (noEdges > (noNodes*(noNodes-1))/2)  :
                tkMessageBox.showwarning("Warning","Entry for edges provided is more than a complete graph." )
                return
        else:
            tkMessageBox.showwarning("Warning","Entry for edges is not an integer.")
            return
        
        self.tree = SCG.StronglyChordalGraph(noNodes, noEdges) #create an instance of StronglyChordalGraph class
        self.tree.createTree()
        self.Tree = True
        
    def onViewTreeClick(self):
        """function to call plotTree"""
        if self.Tree:
            self.tree.plotTree()
        else:
            tkMessageBox.showwarning("Warning","Create (Chordal) Tree first to view (Chordal) Tree.")
            return
        
    def onCreateCGClick(self):
        """function to call createCG"""
        if self.Tree:
            self.tree.createCG()
            self.CG = True
        else:
            tkMessageBox.showwarning("Warning","Create (Chordal) Tree first before create Chordal Graph.")
            return    
    
    def onViewCGClick(self):
        """function to call plotCG"""
        if self.CG:
            self.tree.plotCG()
        else:
            tkMessageBox.showwarning("Warning","Create Chordal Graph first to view Chordal Graph.")
            return        
        
    def onCreateSCGClick(self):
        """function to call createSCG"""
        if self.Tree or self.CG:
            self.tree.createSCG()
            self.SCG = True
        else:
            tkMessageBox.showwarning("Warning","Create (Chordal) Tree or Chordal Graph first before create Strongly Chordal Graph.")
            return
    
    def onViewSCGClick(self):
        """function to call plotSCG"""
        if self.SCG:
            self.tree.plotSCG()
        else:
            tkMessageBox.showwarning("Warning","Create Strongly Chordal Graph first to view Strongly Chordal Graph.")
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
    app.geometry('350x125')#window size
    center(app)
    app.mainloop()
    app.quit()