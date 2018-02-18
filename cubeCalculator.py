from cubeGlobal import cube_u


class BlockEx:
    def __init__(self,b):
        self.block = b
        self.faceColors = []
    def buildFaceColors(self):
        #[0,1,2,3,4,5]分别对应[R,B,L,F,U,D]面
        self.faceColors = []
        b = self.block
        if (b.current.x == -1):
            self.faceColors.append(("F",b.colors[0]))
        if (b.current.x == 1):
            self.faceColors.append(("B",b.colors[0]))
        if (b.current.y == -1):
            self.faceColors.append(("D",b.colors[1]))
        if (b.current.y == 1):
            self.faceColors.append(("U",b.colors[1]))
        if (b.current.z == -1):
            self.faceColors.append(("R",b.colors[2]))
        if (b.current.z == 1):
            self.faceColors.append(("L",b.colors[2]))
         
    def getLayer(self):
        return 1-self.block.current.y
    def isCenter(self):
        b = self.block.current
        n = b.x*b.x + b.y*b.y + b.z*b.z
        return (n==1) 
    def isEdge(self):
        b = self.block.current
        n = b.x*b.x + b.y*b.y + b.z*b.z
        return (n==2) 
    def isCorner(self):
        b = self.block.current
        n = b.x*b.x + b.y*b.y + b.z*b.z
        return (n==3)
    def getFaceColors(self):
        self.buildFaceColors()
        return self.faceColors            
         

class CubeCalculator:
    def __init__(self, cube):
        self.cube = cube
        self.blocks = []
        self.faces = []
        for b in cube.blocks: 
            self.blocks.append(BlockEx(b))
            
                               
    def updateFaces(self):
        self.faces = []
        for b in self.blocks:
            if b.isCenter():
                self.faces.append(b.getFaceColors()[0])
                               
    def matchFaces(self,block_faces, match_all=True, face_to_match = None):
        self.updateFaces()        
        if match_all:                               
            for bf in block_faces:
                print(bf)
                match = [item for item in self.faces if bf == item]
                if match == []:
                    return False
        else:
            for bf in block_faces:
                match = [item for item in self.faces if item == face_to_match]
                if match == []:
                    return False                               
        return True
        
    def isZeroPhase(self):
        for b in self.blocks:
            if b.getLayer() == 2:
                fc = b.getFaceColors()
                if b.isCenter():
                    if fc != ("D","w"):
                        return True
        return False
        
    def isInitPhase(self):
        for b in self.blocks:
            if b.getLayer() == 2:
                fc = b.getFaceColors()
                if b.isEdge():
                    if ("D","w") not in b.getFaceColors():
                        return True
        return False
    def isF2LPhase(self):
        for b in self.blocks:
            if b.getLayer() > 0:
                block_faces = b.getFaceColors() 
                if not self.matchFaces(block_faces):
                    return True
        return False

    def isOLLPhase(self):
        for b in self.blocks:
            if b.getLayer() == 0:
                block_faces = b.getFaceColors() 
                if not self.matchFaces(block_faces,False,("U","y")):
                    return True
        return False
                               
    def isPLLPhase(self):
        for b in self.blocks:
            if b.getLayer() == 0:
                block_faces = b.getFaceColors() 
                if not self.matchFaces(block_faces):
                    return True
        return False



    def calcPhase(self):
        if self.isZeroPhase(): 
            return "ZERO"
        if self.isInitPhase(): 
            return "INIT"
        if self.isF2LPhase():
            return "F2L"
        if self.isOLLPhase():
            return "OLL"
        if self.isPLLPhase():
            return "PLL"
        return "END"
                           
    def calcZeroNextStep(self):
        for b in self.blocks:
            if b.isCenter():
                fc = b.getFaceColors()
                c = [ item for item in fc if item[1] == 'w']
                if c != []:
                    break
        if c != []:
            c_map = {"U":"xx","F":"x'","B":"x'","R":"z","L":"z'","D":"None"}
            return c_map[c[0][0]]
        else:
            return "N/A"

    def calcInitNextStep(self):
        nb = None
        for b in self.blocks:
            if b.isEdge():
                fc = b.getFaceColors()
                c = [ item for item in fc if item[1] == 'w']
                if c != []:
                    nb = b
                    break
        if nb != None:
            c_map = {"U":"xx","F":"x'","B":"x'","R":"z","L":"z'","D":"None"}
            return c_map[c[0][0]]
        else:
            return "N/A"

    def calcF2LNextStep(self):
        return "N/A"
    def calcOLLNextStep(self):
        return "N/A"
    def calcPLLNextStep(self):
        return "N/A"

    def calcNextStep(self):
        p_map = {"ZERO":self.calcZeroNextStep,"INIT":self.calcInitNextStep,"F2L":self.calcF2LNextStep,"OLL":self.calcOLLNextStep,"PLL":self.calcPLLNextStep}
        phase = self.calcPhase()
        hint = p_map[phase]()
        return phase,hint
        

  
