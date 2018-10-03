# -*- coding: utf-8 -*- 
import math, pygame
from operator import itemgetter
from cubeGlobal import cube_o,faces,colors,background
from cubeCommon import printText
from cubePanel import Panel
from cube3D import Point3D,Cube3D

#0,1,2,3为正面的4个点， 4,5,6,7位背面的4个点
block_v = [(x,y,z) for z in (-0.5,0.5) for y in 
    (0.5,-0.5) for x in (-0.5,0.5)]

#在侧边显示后、下、左三面的信息
l_map = {"FRONT":{"FACE":1}, "UP":{"FACE":5},"RIGHT":{"FACE":2}}

class CubeAnimation(Cube3D):
    def __init__(self, cube,width, height, fov, distance,x_adj,y_adj):
        super(CubeAnimation,self).__init__(cube,width, height, fov, 
			  distance,x_adj,y_adj)	

    #face:"FRONT"/"UP"/"RIGHT", layer:0/1/2, clockwize:1/-1, angle:0~90           
    def rotateLayer(self,face,layer,clockwize,angle):
        blocks = [item for item in self.blocks if 
            (item.block.current.x, item.block.current.y, item.block.current.z)
            in faces[face][layer]]
        
        for b3d in blocks:            
            block_vertices = []
            b = b3d.block
            #print "block = ", (b.current.x,b.current.y,b.current.z)
            for i in range(8):
                point = Point3D(b.current.x + block_v[i][0],
                                b.current.y + block_v[i][1],
                                b.current.z + block_v[i][2])
                r_map = {"FRONT":point.rotateX,"RIGHT":point.rotateZ,"UP":point.rotateY}
                r1 = r_map[face](angle*clockwize)                
                r = r1.rotateY(self.alpha).rotateX(self.gama)
                p = r.project(self.width, self.height, self.fov, self.distance, self.x_adj, self.y_adj)
                block_vertices.append(p)
            b3d.resetVertices(block_vertices)

    def rotateCube(self,face,layer,clockwize,angle):
        if layer <= 2:
            self.rotateLayer(face,layer,clockwize,angle)
        elif layer == 3:
            self.rotateLayer(face,0,clockwize,angle)
            self.rotateLayer(face,1,clockwize,angle)
        elif layer == 4:
            self.rotateLayer(face,0,clockwize,angle)
            self.rotateLayer(face,1,clockwize,angle)
            self.rotateLayer(face,2,clockwize,angle)
        elif layer == 5:
            self.rotateLayer(face,1,clockwize,angle)
            self.rotateLayer(face,2,clockwize,angle)
  
    #返回cube显示的区域，在动画过程中要清除这个区域，然后才重新绘制
    def clearCube(self):
        pygame.draw.circle(self.screen,background,(int(self.x_scale*390), int(self.y_scale*345)),int((self.x_scale+self.y_scale)*120))
                    
    def hitBlock(self,x,y):
        for b in self.blocks:
            b1 = b.block
            b2 = cube_o.get((b1.current.x,b1.current.y,b1.current.z))
            if b2 != None:
                for f in b2[1]:
                    if self.hitFace(b,f,x,y):
                        return (b1.current.x,b1.current.y,b1.current.z),f
        return (-2,-2,-2),-1

    def hitFace(self,b,f,x,y):
        p0 = b.vertices[b.faces[f][0]]
        p1 = b.vertices[b.faces[f][1]]
        p2 = b.vertices[b.faces[f][2]]
        p3 = b.vertices[b.faces[f][3]]
        edges = [(p0,p1),(p1,p2),(p2,p3),(p3,p0)]
        cross = []
        ray_point = 0
        for e in edges:#线段方程： y = ax + b
            a = (e[1].y-e[0].y)/(e[1].x-e[0].x+0.1)
            b = (e[0].y*e[1].x - e[1].y*e[0].x)/(e[1].x-e[0].x+0.1)
            cross_y = x*a + b
            if cross_y > y:
                if (x > e[0].x and x < e[1].x) or (x < e[0].x and x > e[1].x):
                    ray_point += 1

        return ray_point == 1        
      
