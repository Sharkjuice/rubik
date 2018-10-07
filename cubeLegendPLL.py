# -*- coding: utf-8 -*- 
import math, pygame
from operator import itemgetter
from cubeGlobal import cube_o,faces,colors,background
from cubeCommon import printText
from cubePanel import Panel
from cube3D import Cube3D

#0,1,2,3为正面的4个点， 4,5,6,7位背面的4个点
block_v = [(x,y,z) for z in (-0.5,0.5) for y in 
    (0.5,-0.5) for x in (-0.5,0.5)]

#在侧边显示后、下、左三面的信息
l_map = {"FRONT":{"FACE":1}, "UP":{"FACE":5},"RIGHT":{"FACE":2}}
       
class CubeLegendPLL(Cube3D):
    def __init__(self, cube,width, height, fov, distance,x_adj,y_adj):
        super(CubeLegendPLL,self).__init__(cube,width, height, fov, 
              distance,x_adj,y_adj) 
            
    def displayLBD(self):
        vs = [20,23,26,26,26,25,24]
        bs = [b for i in vs for b in self.blocks if b.block_id == i]
        vs = [4,4,4,5,1,1,1]
        ps = [bs[i].vertices[vs[i]] for i in range(7)]

        vs = [20,23,26,26,25,24]
        bs = [b for i in vs for b in self.blocks if b.block_id == i]
        vs = [2,2,2,1,1,1]
        cs1 = [bs[i].colors[vs[i]] for i in range(6)]
        
        vs = [11,14,17,17,16,15]
        bs = [b for i in vs for b in self.blocks if b.block_id == i]
        vs = [2,2,2,1,1,1]
        cs2 = [bs[i].colors[vs[i]] for i in range(6)]
        w = 5*self.y_scale
        rs1 = [((ps[i].x,ps[i].y-w), (ps[i+1].x,ps[i+1].y-w),
               (ps[i+1].x,ps[i+1].y-2*w),(ps[i].x,ps[i].y-2*w))
               for i in range(6)]
        rs2 = [((ps[i].x,ps[i].y), (ps[i+1].x,ps[i+1].y),
               (ps[i+1].x,ps[i+1].y-w), (ps[i].x,ps[i].y-w))
               for i in range(6)]

        for i in range(6):
            pygame.draw.polygon(self.screen,cs1[i],rs1[i])
            pygame.draw.polygon(self.screen,(0,0,0),rs1[i],2) 

        for i in range(6):
            pygame.draw.polygon(self.screen,cs2[i],rs2[i])
            pygame.draw.polygon(self.screen,(0,0,0),rs2[i],2) 
            
    #只显示魔方最上一层
    def displayContent(self):
        avg_z = []
        b_i = 0
        top = [b for b in self.blocks if b.block.origin.y != -1]
        for b in top:
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
            t = top[b_i].vertices
            f = top[b_i].faces[f_i]
            c = top[b_i].colors[f_i]

            if c != "-":
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                         (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y)]
                
                pygame.draw.polygon(Panel.screen,c,pointlist)
                pygame.draw.polygon(Panel.screen,(0,0,0),pointlist,2)
        self.displayLBD()

    def hitMe(self,x,y):
        ps = self.outline()
        es = [(ps[i],ps[i+1]) for i in range(6)]
        cross = []
        ray_point = 0
        for e in es:#线段方程： y = ax + b
            a = (e[1].y-e[0].y)/(e[1].x-e[0].x+0.1)
            b = (e[0].y*e[1].x - e[1].y*e[0].x)/(e[1].x-e[0].x+0.1)
            cross_y = x*a + b
            if cross_y > y:
                if (x > e[0].x and x < e[1].x) or (x < e[0].x and x > e[1].x):
                    ray_point += 1
        return ray_point == 1        
    
    def outline(self):
        vs = [9,11,20,26,24,15,9]     
        bs = [b for i in vs for b in self.blocks if b.block_id == i]
        vs = [2,6,4,5,1,3,2]
        ps = [bs[i].vertices[vs[i]] for i in range(7)]
        return ps        
      
    def redraw(self):
        ps = self.outline()     
        pointlist =[(ps[i].x,ps[i].y) for i in range(6)] 
        pygame.draw.polygon(self.screen,(0,0,0),pointlist,4)
        self.displayContent()      
    def drawSelected(self):
        ps = self.outline()     
        pointlist =[(ps[i].x,ps[i].y) for i in range(6)] 
        pygame.draw.polygon(self.screen,(244,244,244),pointlist,4)
        