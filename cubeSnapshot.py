# -*- coding: utf-8 -*-  
import pygame,copy
import cubeView,cubeModel
from cubeCommon import button,printText,printRight
from cubeGlobal import background,screen,green,black,\
	 gray,colors,getDisplayParams

#显示魔方区域的高度和宽度
height = 500
width = 500
#3D显示参数
fov = 700
distance = 12
adj_x = 830
adj_y = 50
	
class CubeSnapshot:
    def __init__(self,cube):
        global height,width,fov,distance,adj_x,adj_y
        self.total =  0
        self.total_page = 0
        self.current = -1
        self.current_page = -1
        self.next_index = 0
        self.snapshots = []
        self.level = 0		
        self.my_cube_3d = cubeView.Cube3D(cube,width,
		    height, fov, distance, adj_x, adj_y)
		
    def takeSnapshot(self,cube):
        self.my_cube_3d.cube = copy.deepcopy(cube)
        self.my_cube_3d.buildFaces()
        self.displayCube()
        
    def displayCube(self):   
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLayer("RIGHT",2, 180,-70)
        self.my_cube_3d.displayLayer("UP",2, 160, 260)
        self.my_cube_3d.displayLayer("FRONT",2, 480, -70)
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        b_x = x_scale*1160
        b_y = y_scale*640
        b_h = y_scale*30
        printRight("快照窗口")

    def cube(self):
        return self.my_cube_3d.cube 

    def blocks(self):
        return self.my_cube_3d.blocks
