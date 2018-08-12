# -*- coding: utf-8 -*-  
import pygame,copy
import cubeView,cubeModel
from cubeCommon import button,printText
from cubeGlobal import background,screen,green,black,\
	bright_green,gray,colors,getDisplayParams

class CubeSnapshot:
    def __init__(self,cube,width, height, fov, distance,x_adj,y_adj):
        self.total =  0
        self.total_page = 0
        self.current = -1
        self.current_page = -1
        self.next_index = 0
        self.snapshots = []
        self.level = 0		
        self.x_adj = x_adj
        self.y_adj = y_adj
        self.width = width
        self.height = height
        self.fov = fov
        self.distance = distance
        self.sn_cube_3d = cubeView.Cube3D(cube,width, height, fov, distance, x_adj,y_adj)
		
    def takeSnapshot(self,cube):
        self.sn_cube_3d.cube = copy.deepcopy(cube)
        self.sn_cube_3d.buildFaces()
        self.displayCube()
        
    def displayCube(self):   
        self.sn_cube_3d.displayCube()
        self.sn_cube_3d.displayLayer("RIGHT",2, 180,-70)
        self.sn_cube_3d.displayLayer("UP",2, 160, 260)
        self.sn_cube_3d.displayLayer("FRONT",2, 480, -70)
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        b_x = x_scale*1160
        b_y = y_scale*640
        b_h = y_scale*30
        pygame.draw.rect(screen,gray,(b_x, b_y, x_scale*180,b_h))            
        printText(screen, "快照窗口", "fangsong", ft_sz, b_x + 5, 
		    b_y + 3, black)
