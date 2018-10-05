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
       
class CubeLegendF2L(Cube3D):
    def __init__(self, cube,width, height, fov, distance,x_adj,y_adj):
        super(CubeLegendF2L,self).__init__(cube,width, height, fov, 
              distance,x_adj,y_adj) 

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
        if ray_point == 1:
            pointlist =[(ps[i].x,ps[i].y) for i in range(6)] 
            pygame.draw.polygon(self.screen,(244,244,244),pointlist,4) 
        return ray_point == 1        
    
    def outline(self):
        vs = [0,2,20,26,24,6,0]     
        bs = [b for i in vs for b in self.blocks if b.block_id == i]
        vs = [2,6,4,5,1,3,2]
        ps = [bs[i].vertices[vs[i]] for i in range(7)]
        return ps        
      
    def redraw(self):
        ps = self.outline()     
        pointlist =[(ps[i].x,ps[i].y) for i in range(6)] 
        pygame.draw.polygon(self.screen,(0,0,0),pointlist,4)
        self.displayCube()		
        