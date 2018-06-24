# -*- coding: utf-8 -*-  
import pygame,copy,math
from cubeGlobal import background,screen,green,bright_green,gray,colors,getDisplayParams
from cubeCommon import button
import cubeView,cubeModel


class CubeSnapshot:
    def __init__(self,cube,width, height, fov, distance,x_adj,y_adj):
        self.total =  0
        self.total_page = 1
        self.current = -1
        self.current_page = 1
        self.x_adj = x_adj
        self.y_adj = y_adj
        self.width = width
        self.height = height
        self.fov = fov
        self.distance = distance
        self.sn_cube_3d = cubeView.Cube3D(cube,width, height, fov, distance, x_adj,y_adj)
    
    def selectSnapshot(self,b):        
        self.current = b
        fo = open(".\\snapshots\\mycube" + str(b) + ".clp", "r", 1)
        blocks = []
        if fo != None:
            for line in fo.readlines():
                b = line.strip("(\n)").split(" ")
                if b[0] == "assert" and b[1] == "(blk":
                    blocks.append(((int(b[2]),int(b[3]),int(b[4])),"".join([b[5],b[6],b[7]])))
            fo.close()
            cube = cubeModel.Cube(blocks)
            self.sn_cube_3d = cubeView.Cube3D(cube,self.width, self.height, self.fov, 
                self.distance,self.x_adj,self.y_adj)
            
            self.displayCube()
    
    def setTotal(self,t):        
        self.total = t
        m,r = divmod(t,10)
        if (m + r) != 0:
            if r == 0:
                self.total_page = m
            else:
                self.total_page = m + 1
        
    def nextPage(self,flag):
        if self.current_page < self.total_page:
            self.current_page += 1
    def prevPage(self,flag):
        if self.current_page > 0:
            self.current_page -= 1
            
    def displayHeader(self):
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        b_x = x_scale*810
        b_y = y_scale*10
        b_h = y_scale*30
        if self.total_page == 0:
            start = 0
            stop1 = 0
            stop2 = 10        
        else:
            start = (self.current_page -1)*10
            stop1 = start + 10
            stop2 = stop1        
            if self.current_page == self.total_page:
                stop1 = self.total
        if self.current_page == 1:
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,b_h,gray,bright_green,self.prevPage,-1)
        else:
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,b_h,green,bright_green,self.prevPage,-1)
        b_x += x_scale*40

        for b in range(start,stop1):
            button(screen, str(b+1), ft_sz, b_x, b_y, x_scale*30,b_h,green,bright_green,self.selectSnapshot,b+1)
            b_x += x_scale*40
        for b in range(stop1, stop2):
            button(screen, "", ft_sz, b_x, b_y, x_scale*30,b_h,gray,bright_green,self.selectSnapshot,b+1)
            b_x += x_scale*40
        if self.current_page == self.total_page:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,b_h,gray,bright_green,self.nextPage,1)
        else:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,b_h,green,bright_green,self.nextPage,1)
        
    def takeSnapshot(self,cube):
        snapshot_cube_mode = copy.deepcopy(cube)
        self.sn_cube_3d.cube = snapshot_cube_mode
        
    def displayCube(self):   
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        self.sn_cube_3d.buildFaces()
        #pygame.draw.rect(screen,background,(x_scale*810,y_scale*5,x_scale*538,y_scale*595))    
        self.sn_cube_3d.displayCube()
        self.sn_cube_3d.displayLayer("RIGHT",2, 180,-70)
        self.sn_cube_3d.displayLayer("UP",2, 160, 260)
        self.sn_cube_3d.displayLayer("FRONT",2, 480, -70)
