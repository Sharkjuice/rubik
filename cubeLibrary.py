# -*- coding: utf-8 -*-  
import pygame,copy,math,os
from cubeGlobal import background,screen,green,black,\
	red,gray,colors,getDisplayParams
from cubeCommon import button,printLeft,printRight
import cubeView,cubeModel

#显示魔方区域的高度和宽度
height = 500
width = 500
#3D显示参数
fov = 700
distance = 12
adj_x = 820
adj_y = 50

s_map = {0:u"自定义题库",1:u"十字底题库",2:u"F2L题库",3:u"OLL题库",4:u"PLL题库"}

class CubeLibrary:
    def __init__(self,cube):
        global height,width,fov,distance,adj_x,adj_y
        self.total =  0
        self.total_page = 0
        self.current = -1
        self.current_page = -1
        self.next_index = 0
        self.snapshots = []
        self.lib_level = 0	
        self.my_cube_3d = cubeView.Cube3D(cube,width, 
			height, fov, distance, adj_x, adj_y)
        self.snapshots_dir = ".\\snapshots_0\\"
        self.build()
		
    def build(self):	
        self.snapshots = []	
        try:
            with open(self.snapshots_dir + "index", "r",1) as fo:
                for line in fo.readlines():
                    b = line.strip("(\n)").split(" ")
                    if b[0] != "" and b[0][0] != "#":
                        self.snapshots.append((b[0],int(b[1])))
        except IOError as err: 
            os.mkdir(self.snapshots_dir)		
            fo = open(self.snapshots_dir + "index", "w", 1)
            fo.write("#generated by this program, never modify it.\n")
            fo.close()   
        if len(self.snapshots) > 0:
            self.setTotal(len(self.snapshots))
            self.setCurrent(1)		
            last = self.snapshots[-1][0]
            last_index = int(last[7:-4])
            self.next_index = last_index
        else:
            self.total =  0
            self.total_page = 0
            self.current = -1
            self.current_page = -1
            self.next_index = 0

    def saveCube(self,cube,flag,figure=0):
        if figure != 0:#此图案已经存在，就不保存了。
            if figure in [item[1] for item in self.snapshots]:
               return u"已经有相同的魔方存在，不能保存"
        if flag == 0:#临时存放，为了调用规则引擎
            fo = open(".\\mycube.clp", "w", 1)
        else:
            self.next_index += 1
            new_sn = "mycube_" + str(self.next_index) + ".clp"
            fs = open(self.snapshots_dir +"index", "a", 1)
            new_item = new_sn + " " + str(figure)
            fs.write(new_item + "\n")
            fs.close()
            self.setTotal(self.total + 1)
            self.snapshots.append((new_sn,figure))
            fo = open(self.snapshots_dir + "mycube_" + str(self.next_index) + ".clp", "w", 1)
            self.takeSnapshot(cube)
            self.setCurrent(self.getTotal())
        fo.write("(defrule start-up =>\n")
        for block in cube.blocks:
            block_str = "(assert (blk %d %d %d %c %c %c))\n" % (block.current.x, block.current.y, block.current.z,
              block.colors[0],block.colors[1],block.colors[2])
            fo.write(block_str)
        fo.write("\n(assert (phase 0)))")
        fo.close()
        return u"保存为第" + str(self.total) + "份快照"

    def deleteSnapshot(self):  
        if self.lib_level > 0:
            return u"不能删除非自定义题库里的题目"	
        if self.total == 0 or self.current == 0:
            return
        os.remove(self.snapshots_dir +  self.snapshots[self.current-1][0])
        del(self.snapshots[self.current-1])
        with open(self.snapshots_dir + "index", "w", 1) as fo:
            fo.write("#generated by this program, never modify it.\n")
            for line in self.snapshots:
                fo.write(line[0] + " " + str(line[1]) + "\n")
        self.setTotal(self.total - 1)
        if self.current > 0:
            self.setCurrent(self.current - 1)
        if self.current == 0:
            self.setCurrent(self.current + 1)
        self.selectSnapshot(self.current)
		
    def selectSnapshot(self,b=None):        
        if self.total == 0:
            return		
        if b != None:#default select current， which is default to 0
            self.current = b
        fo = open(self.snapshots_dir + self.snapshots[self.current-1][0], "r", 1)
        blocks = []
        if fo != None:
            for line in fo.readlines():
                b = line.strip("(\n)").split(" ")
                if b[0] == "assert" and b[1] == "(blk":
                    blocks.append(((int(b[2]),int(b[3]),int(b[4])),"".join([b[5],b[6],b[7]])))
            fo.close()
            cube = cubeModel.Cube(blocks)
            self.my_cube_3d.cube = copy.deepcopy(cube)				
            self.my_cube_3d.buildFaces()
            self.displayCube()
			
    def setCurrent(self,c):
        if self.total == 0:
            return		
        self.current = c
        m,r = divmod(c,10)
        if (m + r) != 0:
            if r == 0:
                self.current_page = m
            else:
                self.current_page = m + 1        
		
    
    def setTotal(self,t):        
        self.total = t
        m,r = divmod(t,10)
        if (m + r) != 0:
            if r == 0:
                self.total_page = m
            else:
                self.total_page = m + 1
				
    def getTotal(self):        
        return self.total 
		
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
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,b_h,gray,red,None,-1)
        else:
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,b_h,green,red,self.prevPage,-1)
        b_x += x_scale*40

        for b in range(start,stop1):
            if (b + 1) == self.current:		
                button(screen, str(b+1), ft_sz, b_x, b_y, x_scale*30,b_h,red,red,self.selectSnapshot,b+1)
            else:
                button(screen, str(b+1), ft_sz, b_x, b_y, x_scale*30,b_h,green,red,self.selectSnapshot,b+1)
            b_x += x_scale*40
        for b in range(stop1, stop2):
            button(screen, "", ft_sz, b_x, b_y, x_scale*30,b_h,gray,red,None,b+1)
            b_x += x_scale*40
        if self.current_page == self.total_page:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,b_h,gray,red,None,1)
        else:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,b_h,green,red,self.nextPage,1)

        b_x = x_scale*810
        b_y = y_scale*640
        #显示控制按钮
        b_map = [("自定",self.level,0),("十字",self.level,1),("F2L",self.level,2),
                    ("OLL",self.level,3),(u"PLL",self.level,4)]

        b_x = x_scale*810; b_y = y_scale*640; b_h = y_scale*30
        for b in b_map:
            button(screen, b[0], ft_sz, b_x, b_y, x_scale*60,b_h,green,red,b[1],b[2])
            b_x += x_scale*70
        printRight(s_map[self.lib_level])
		
    def takeSnapshot(self,cube):
        self.my_cube_3d.cube = copy.deepcopy(cube)
        self.my_cube_3d.buildFaces()
        self.displayCube()
        
    def displayCube(self):   
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLayer("RIGHT",2, 180,-70)
        self.my_cube_3d.displayLayer("UP",2, 160, 260)
        self.my_cube_3d.displayLayer("FRONT",2, 480, -70)

    def level(self,value):
        self.setLevel(value)
        self.selectSnapshot()
		
    def setLevel(self,value):
        self.lib_level = value
        self.snapshots_dir = ".\\snapshots_" + str(value) + "\\"
        self.build()
        printRight(s_map[self.lib_level])

    def cube(self):
        return self.my_cube_3d.cube 

    def blocks(self):
        return self.my_cube_3d.blocks
	