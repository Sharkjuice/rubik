# -*- coding: utf-8 -*-  
from cubeGlobal import faces
#x轴：水平向右；y轴：垂直向上；z轴：向屏幕里面，圆心在魔方中心块
cube_i = [
    ((-1, -1, -1), "rwg"), ((-1, 0, -1), "r-g"), ((-1, 1, -1), "ryg"), 
    ((-1, -1,0), "rw-"), ((-1, 0, 0), "r--"), ((-1, 1, 0), "ry-"), 
    ((-1, -1, 1), "rwo"), ((-1, 0, 1), "r-o"), ((-1, 1, 1), "ryo"),
    
    ((0, -1, -1), "-wg"), ((0, 0, -1), "--g"), ((0, 1, -1), "-yg"), 
    ((0, -1, 0), "-w-"), ((0, 0, 0), "---"), ((0, 1, 0), "-y-"), 
    ((0, -1, 1), "-wo"), ((0, 0, 1), "--o"), ((0, 1, 1), "-yo"),

    ((1, -1, -1), "bwg"), ((1, 0, -1), "b-g"), ((1, 1, -1), "byg"), 
    ((1, -1, 0), "bw-"), ((1, 0, 0), "b--"), ((1, 1, 0), "by-"), 
    ((1, -1, 1), "bwo"), ((1, 0, 1), "b-o"), ((1, 1, 1), "byo")
]

class Point:
    def __init__(self, x, y, z):
        self.x,self.y,self.z = x,y,z
    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return self.__dict__ == other.__dict__
        if type(other) == tuple:
            return (self.x,self.y,self.z) == other
    def __ne__(self,other):
        if isinstance(other,self.__class__):
            return self.__dict__ != other.__dict__       
        if type(other) == tuple:
            return (self.x,self.y,self.z) != other

class Block:
    def __init__(self, x, y, z, colors):
        self.current = Point(x,y,z) 
        self.origin = Point(x,y,z)
        self.colors = [c for c in colors]
        
     
class Cube:
    def __init__(self, cube = cube_i):
        self.blocks = []
        for aBlock in cube:
            block = Block(aBlock[0][0],aBlock[0][1],aBlock[0][2],aBlock[1])
            self.blocks.append(block)
 
    #沿x轴反时针转
    def rotateX(self,block,clockwize = 1):
        """ Rotates the point around the X axis by 90. """
        tmp = block.current.y
        if clockwize == 1:            
            block.current.y = -block.current.z  
            block.current.z = tmp            
        else:            
            block.current.y = block.current.z  
            block.current.z = -tmp
        tmp = block.colors[2]
        block.colors[2] = block.colors[1]
        block.colors[1] = tmp
        
     #沿y轴顺时针转，注意和x、z轴不一样
    def rotateY(self, block,clockwize = True):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        tmp = block.current.z
        if clockwize == 1:
            block.current.z = -block.current.x
            block.current.x = tmp
        else:
            block.current.z = block.current.x
            block.current.x = -tmp       
        tmp = block.colors[2]
        block.colors[2] = block.colors[0]
        block.colors[0] = tmp
    #沿z轴逆时针转
    def rotateZ(self, block,clockwize = True):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        tmp = block.current.x
        if clockwize == 1:
            block.current.x = -block.current.y
            block.current.y = tmp
        else:
            block.current.x = block.current.y
            block.current.y = -tmp
        tmp = block.colors[1]
        block.colors[1] = block.colors[0]
        block.colors[0] = tmp

    #沿YZ平面镜像
    def mirrorCube(self):
        """ Reflects around YZ plane. """
        for b in self.blocks:
            b.current.x = -b.current.x  
        
    def rotateLayer(self,face,layer,clockwize):
        r_map = {"FRONT":self.rotateX,"RIGHT":self.rotateZ,"UP":self.rotateY}
        blocks = [item for item in self.blocks if  
                (item.current.x, item.current.y, item.current.z)
                in faces[face][layer]]
        for b in blocks:
            r_map[face](b,clockwize)          

    def rotateCube(self,face,layer,clockwize):
        if layer <= 2:
            self.rotateLayer(face,layer,clockwize)
        elif layer == 3:
            self.rotateLayer(face,0,clockwize)
            self.rotateLayer(face,1,clockwize)
        elif layer == 4:
            self.rotateLayer(face,0,clockwize)
            self.rotateLayer(face,1,clockwize)
            self.rotateLayer(face,2,clockwize)
        elif layer == 5:
            self.rotateLayer(face,1,clockwize)
            self.rotateLayer(face,2,clockwize)
        elif layer == 6:
            self.mirrorCube()
            
    def validateCube(self):
        colors = {"w":0,"y":0,"r":0,"b":0,"g":0,"o":0,"-":1}
	         		
        #map(count_colors, self.blocks)
        for b in self.blocks:
            for c in b.colors:
                if c != "-":
                    colors[c] += 1
        v = 1
        for c,x in colors.items():
            v *= x
        #print("Total value ", v)
        if v != 531441:
            return False
        else:
            return True		
        
  

