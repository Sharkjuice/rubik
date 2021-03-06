# -*- coding: utf-8 -*- 
import math, pygame
from operator import itemgetter
from cubeGlobal import cube_o,faces,colors,background
from cubeCommon import printText
from cubePanel import Panel

#0,1,2,3为正面的4个点， 4,5,6,7位背面的4个点
block_v = [(x,y,z) for z in (-0.5,0.5) for y in 
    (0.5,-0.5) for x in (-0.5,0.5)]

#在侧边显示后、下、左三面的信息
l_map = {"FRONT":{"FACE":1}, "UP":{"FACE":5},"RIGHT":{"FACE":2}}

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)

    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)

    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)

    def project(self, win_width, win_height, fov, viewer_distance, offsetX=0, offsetY=0):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x + offsetX, y + offsetY, self.z)
    def scale(self,x_offset, y_offset,factor):
        x = self.x*factor
        y = self.y*factor
        return Point3D(x + x_offset, y + y_offset, self.z)

class Block3D:
    def __init__(self,vertices,faces,b):
        self.vertices = vertices
        self.faces = faces
        self.block = b
        self.colors = [colors["-"]]*6
        self.mark = "-"
		#给方块编号，从下到上分层，层内从FR角，从1开始
        self.block_id = (b.current.z + 1) + \
			  (b.current.x + 1)*3 + (b.current.y + 1)*9

    def resetVertices(self,vertices):
        self.vertices = vertices
        return self
    def resetColors(self):
        b = self.block
        if (b.current.x == -1):
            self.colors[3] = colors[b.colors[0]]
        if (b.current.x == 1):
            self.colors[1] = colors[b.colors[0]]
        if (b.current.y == -1):
            self.colors[5] = colors[b.colors[1]]
        if (b.current.y == 1):
            self.colors[4] = colors[b.colors[1]]
        if (b.current.z == -1):
            self.colors[0] = colors[b.colors[2]]
        if (b.current.z == 1):
            self.colors[2] = colors[b.colors[2]]
        return self
        
class Cube3D:
    def __init__(self, cube,width, height, fov, distance,x_adj,y_adj):
        self.screen,self.x_scale,self.y_scale = \
         Panel.screen,Panel.x_scale,Panel.y_scale
        self.cube = cube
        self.blocks = []
        self.alpha = -45
        self.gama = -30
        self.beta = 0
        self.width = self.x_scale*width
        self.height = self.y_scale*height
        self.fov = (self.x_scale+self.y_scale)*fov/2
        self.distance = distance
        self.x_adj = self.x_scale*x_adj
        self.y_adj = self.y_scale*y_adj

    def buildFaces(self):
        self.blocks = []
        for b in self.cube.blocks:
            block_vertices = []
            for i in range(8):
                point = Point3D(b.current.x + block_v[i][0],
                                b.current.y + block_v[i][1],
                                b.current.z + block_v[i][2])
                r = point.rotateY(self.alpha).rotateX(self.gama).rotateY(self.beta)
                p = r.project(self.width, self.height, self.fov, self.distance, self.x_adj,self.y_adj )
                block_vertices.append(p)
            #各面的顶点。 数组中的顺序为：F/B/L/R/U/D
            block_faces = [(0,1,3,2),(1,5,7,3),(5,4,6,7),(4,0,2,6),(0,4,5,1),(2,3,7,6)]
            
            self.blocks.append(Block3D(block_vertices,block_faces,b).resetColors())
    def setLBDPos(self,pos):
        scaled_pos = [(p[0]*self.x_scale,p[1]*self.y_scale) for p in pos]	    
        self.lbd_pos = {"RIGHT":scaled_pos[0],"FRONT":scaled_pos[1],
				        "UP":scaled_pos[2]}
            
    def displayLayer(self,face,layer):
        face_index = l_map[face]["FACE"]
        (x_offset, y_offset) = self.lbd_pos[face]
        
        blocks = [item for item in self.blocks if 
            (item.block.current.x, item.block.current.y, item.block.current.z)
            in faces[face][layer]]
        for b in blocks:
            t = []
            for point in b.vertices:
                p = point.scale(x_offset, y_offset,0.7)
                t.append(p)
            c = b.colors[face_index]
            f = b.faces[face_index]
            pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                     (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y)]                
            pygame.draw.polygon(self.screen,c,pointlist)
            pygame.draw.polygon(self.screen,(0,0,0),pointlist,2) 
            if  b.mark != "-":
                if c == (0,0,255):#蓝色的块，要先是白色的字，不然看不清
                    printText(self.screen,b.mark, "kaiti", 20, int((t[f[0]].x + t[f[2]].x)/2.0)-5 , int((t[f[0]].y + t[f[2]].y)/2.0)-10, (255,255,255))
                else:
                    printText(self.screen,b.mark, "kaiti", 20, int((t[f[0]].x + t[f[2]].x)/2.0)-5 , int((t[f[0]].y + t[f[2]].y)/2.0)-10, (0,0,0))
    #在正中间显示魔方的主体，立体显示，通过视角控制，显示前面、右面、上面
    def displayCube(self):
        avg_z = []
        b_i = 0

        for b in self.blocks:
            f_i = 0
            for f in b.faces:
                z = (b.vertices[f[0]].z + b.vertices[f[1]].z +
                 b.vertices[f[2]].z + b.vertices[f[3]].z) / 4.0
                avg_z.append((b_i,f_i,z))
                f_i = f_i + 1
            b_i = b_i + 1

        # Draw the faces using the Painter's algorithm:
        # Distant faces are drawn before the closer ones.
        for tmp in sorted(avg_z,key=itemgetter(2),reverse=True):
            b_i = tmp[0]
            f_i = tmp[1]
            t = self.blocks[b_i].vertices
            f = self.blocks[b_i].faces[f_i]
            c = self.blocks[b_i].colors[f_i]

            if c != "-":
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                         (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y)]
                
                pygame.draw.polygon(Panel.screen,c,pointlist)
                pygame.draw.polygon(Panel.screen,(0,0,0),pointlist,2)
                
                if  self.blocks[b_i].mark != "-":
                    if c == (0,0,255):#蓝色的块，要先是白色的字，不然看不清
                        printText(Panel.screen,self.blocks[b_i].mark, "kaiti", 20, int((t[f[0]].x + t[f[2]].x)/2.0)-5 , int((t[f[0]].y + t[f[2]].y)/2.0)-10, (255,255,255))
                    else:
                        printText(Panel.screen,self.blocks[b_i].mark, "kaiti", 20, int((t[f[0]].x + t[f[2]].x)/2.0)-5 , int((t[f[0]].y + t[f[2]].y)/2.0)-10, (0,0,0))
            
    def displayContent(self):
        self.displayCube()
        self.displayLayer("RIGHT",2)
        self.displayLayer("UP",2)
        self.displayLayer("FRONT",2)
