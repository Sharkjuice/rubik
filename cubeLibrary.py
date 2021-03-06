# -*- coding: utf-8 -*-  
import pygame,copy,math,os
from cubeGlobal import background,green,black,red,colors
from cubeCommon import button
from cubePanel import Panel
import cubeModel,cubeLegendF2L,cubeLegendOLL,cubeLegendPLL

#显示魔方区域的高度和宽度
height = 500
width = 500
#3D显示参数
fov = 700
distance = 12
adj_x = 830
adj_y = 50

s_map = {0:u"自定义题库",1:u"十字底题库",2:u"F2L题库",3:u"OLL题库",4:u"PLL题库"}

class CubeLibrary:
    def __init__(self,cube,init_level=0):
        self.total =  0
        self.total_page = 0
        self.current = 1
        self.current_page = 1
        self.next_index = 0
        self.snapshots = []
        self.my_cube_3d = None
        self.snapshots_dir = ".\\snapshots_0\\"
        self.legends = []
        self.current_legend = -1
        self.total_legend = 0
        
        #鼠标点击状态
        self.single_clicked = False
        self.lib_level = 0
        self.setLevel(init_level)
        
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
            self.setCurrent((1,-1))      
            last = self.snapshots[-1][0]
            last_index = int(last[7:-4])
            self.next_index = last_index
        else:
            self.total =  0
            self.total_page = 0
            self.current = 1
            self.current_page = 1
            self.next_index = 0
            
    def writeCube2File(self,dir,file_no,cube,figure=0):
        if file_no == -1:
            fn = "mycube" + ".clp"
        else:
            fn = "mycube_" + str(file_no) + ".clp"
            fs = open(dir +"index", "a", 1)
            fs.write(fn + " " + str(figure) + "\n")
            fs.close()
        fo = open(dir + fn, "w", 1)
        fo.write("(defrule start-up =>\n")
        for block in cube.blocks:
            block_str = "(assert (blk %d %d %d %c %c %c))\n" % (block.current.x, block.current.y, block.current.z,
              block.colors[0],block.colors[1],block.colors[2])
            fo.write(block_str)
        fo.write("\n(assert (phase 0)))")
        fo.close()
            
    def saveCube(self,cube):
        self.setLevel(0)        
        self.next_index += 1
        self.writeCube2File(self.snapshots_dir,self.next_index,
                            cube,0)
        self.build()
        Panel.printLeft(u"保存为第" + str(self.total) + "份快照")
        self.setCurrent((self.getTotal(),-1))
        self.displayContent()
    #非界面调用,figure 不为0
    def saveCube2(self,cube,figure):
        if figure == 0:#临时存放，为了调用规则引擎
            f = ".\\mycube.clp"
            self.writeCube2File("./",-1,cube,0)
            return
        else:
            if figure in [item[1] for item in self.snapshots]:
                return
            else:
                self.next_index += 1
                self.writeCube2File(self.snapshots_dir,self.next_index,
                                cube,0)

    def deleteCurrent(self):  
        if self.lib_level > 0:
            Panel.printLeft(u"不能删除非自定义题库里的题目")
            return     
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
            self.setCurrent((self.current - 1,-1))
        if self.current == 0:
            self.setCurrent((self.current + 1,-1))
        self.displayContent()
        
    def showLibBelowLevel3(self):        
        if self.total == 0:
            return      
        self.legends = []           
        file = self.snapshots_dir + self.snapshots[self.current-1][0]
        cube = cubeModel.Cube(file) 
        self.my_cube_3d = cubeLegendF2L.CubeLegendF2L(cube,width, 
                   height, fov, distance, adj_x, adj_y)
        self.my_cube_3d.buildFaces()
        self.my_cube_3d.setLBDPos([(180,-70),(480, -70),  
                                            (160, 260)])    
        self.my_cube_3d.displayContent()
        self.legends.append(self.my_cube_3d)
        self.current_legend = 0 
        Panel.printLeft(u"选择了第" + str(self.current) + "份快照")
    #(-1,-1)缺省显示第一页,无选中，
    #(-1,N)显示第N个图例所在页，并选中第N个图例
    #(N,-1)显示第N页,选中第一个
    #(N1,N2)忽略N1,等同(-1,N2)
    def showLibLevel3(self): 
        if self.total == 0:
            return
        Panel.clearRight()  
        start = (self.current-1)*15
        end = start + 15
        if end > len(self.snapshots):
            end = len(self.snapshots)
        self.legends = []
        for i in range(start,end):
            file_no =  + i
            file = self.snapshots_dir + self.snapshots[i][0]
            cube = cubeModel.Cube(file)   
            m,r = divmod(i-start,3)           
            cube_3d = cubeLegendOLL.CubeLegendOLL(cube,width, 
                   height, fov, 20, 650+r*180, -120+m*115)
            cube_3d.buildFaces()
            cube_3d.displayContent()
            self.legends.append(cube_3d)            
    #(-1,-1)缺省显示第一页,无选中，
    #(-1,N)显示第N个图例所在页，并选中第N个图例
    #(N,-1)显示第N页,缺省无选中
    #(N1,N2)忽略N1,等同(-1,N2)
    def showLibLevel4(self): 
        if self.total == 0:
            return
        Panel.clearRight()  
        start = (self.current-1)*12
        end = start + 12
        if end > len(self.snapshots):
            end = len(self.snapshots)
        self.legends = []
        for i in range(start,end):
            file_no =  + i
            file = self.snapshots_dir + self.snapshots[i][0]
            cube = cubeModel.Cube(file)   
            m,r = divmod(i-start,3)           
            cube_3d = cubeLegendPLL.CubeLegendPLL(cube,width, 
                   height, fov, 20, 650+r*180, -120+m*150)
            cube_3d.buildFaces()
            cube_3d.displayContent()
            self.legends.append(cube_3d)            

    def displayContent(self,level_current = None):
        Panel.clearRight()
        Panel.printRight(s_map[self.lib_level])
        self.my_cube_3d = None
        self.single_clicked = False
        if level_current != None:
            self.setLevel(level_current[0])
            self.setCurrent((level_current[1],level_current[2]))        
        if self.lib_level == 3:
            self.showLibLevel3()
        elif self.lib_level == 4:
            self.showLibLevel4()
        else:
            self.showLibBelowLevel3()
        if self.current_legend != -1:
            self.my_cube_3d = self.legends[self.current_legend]
            self.my_cube_3d.drawSelected()
            
    #(-1,-1)缺省显示第一页,无选中，
    #(-1,N)显示第N个图例所在页，并选中第N个图例
    #(N,-1)显示第N页,缺省无选中
    #(N1,N2)忽略N1,等同(-1,N2)
    #N,N1,N2都是从1开始数
    def setCurrent(self,c):
        if self.total == 0:return 
        if c == (-1,-1):return
        if self.lib_level < 3:
            if c[0] != -1:cur = c[0]
            if c[1] != -1:cur = c[1]
            self.current = cur
            self.current_legend = 0 
            m,r = divmod(cur,10)
            if (m + r) != 0:
                if r == 0:
                    self.current_page = m
                else:
                    self.current_page = m + 1        
        elif self.lib_level == 3:
            self.current_page =1
            if c[0] != -1:
                self.current = c[0]
                self.current_legend = -1         
            if c[1] != -1:
                m,r = divmod(c[1] - 1,15)
                self.current = m + 1
                self.current_legend = r         
        elif self.lib_level == 4:
            self.current_page =1
            if c[0] != -1:
                self.current = c[0]
                self.current_legend = -1         
            if c[1] != -1:
                m,r = divmod(c[1] - 1,12)
                self.current = m + 1
                self.current_legend = r 
    
    def setTotal(self,t):  
        if self.lib_level < 3:
            m,r = divmod(t,10)
            self.total = self.total_legend = t
            if (m + r) != 0:
                if r == 0:
                    self.total_page = m
                else:
                    self.total_page = m + 1
        elif self.lib_level == 3:
            self.total_page = 1
            m,r = divmod(t,15)
            self.total = m + 1
            self.total_legend = t
        elif self.lib_level == 4:
            self.total_page = 1
            m,r = divmod(t,12)
            self.total = m + 1
            self.total_legend = t
        
    def getTotal(self):        
        return self.total_legend
        
    def nextPage(self,flag):
        if self.current_page < self.total_page:
            self.current_page += 1
    def prevPage(self,flag):
        if self.current_page > 0:
            self.current_page -= 1
            
    def displayHeader(self):
        screen,ft_sz,x_scale,y_scale= Panel.screen, \
             Panel.ft_sz,Panel.x_scale,Panel.y_scale
        b_x = x_scale*820
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
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,
                                b_h, Panel.gray, red,None,-1)
        else:
            button(screen, "<<", ft_sz, b_x, b_y, x_scale*30,
                              b_h,green,red,self.prevPage,-1)
        b_x += x_scale*40

        for b in range(start,stop1):
            if (b + 1) == self.current:     
                button(screen, str(b+1), ft_sz, b_x, b_y, 
                       x_scale*30,b_h,red,red,self.displayContent,(-1,b+1,-1))
            else:
                button(screen, str(b+1), ft_sz, b_x, b_y,
                       x_scale*30,b_h,green,red,self.displayContent,(-1,b+1,-1))
            b_x += x_scale*40
        for b in range(stop1, stop2):
            button(screen, "", ft_sz, b_x, b_y, x_scale*30,
                   b_h,Panel.gray,red,None,b+1)
            b_x += x_scale*40
        if self.current_page == self.total_page:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,
                   b_h,Panel.gray,red,None,1)
        else:
            button(screen, ">>", ft_sz, b_x, b_y, x_scale*30,
                   b_h,green,red,self.nextPage,1)

        #显示控制按钮
        b_map = [("自定",(0,1,-1)),("十字",(1,1,-1)),("F2L",(2,1,-1)),
                    ("OLL",(3,1,-1)),(u"PLL",(4,1,-1))]

        b_x = x_scale*820
        b_y = y_scale*640
        b_h = y_scale*30
        for b in b_map:
            button(screen, b[0], ft_sz, b_x, b_y, x_scale*60,b_h,green,red,
            self.displayContent,b[1])
            b_x += x_scale*70
        Panel.printRight(s_map[self.lib_level])
        
    def setLevel(self,value):
        if value == -1:
            return
        self.lib_level = value
        self.snapshots_dir = ".\\snapshots_" + str(value) + "\\"
        self.build()

    def cube(self):
        if self.my_cube_3d != None:
            return self.my_cube_3d.cube 
        else:
            return None
    def blocks(self):
        if self.my_cube_3d != None:
            return self.my_cube_3d.blocks 
        else:
            return None
        
    def singleClick(self,x,y):
        if self.legends == []:
            return False
        if self.lib_level < 3:
            if self.my_cube_3d.hitMe(x,y):
                self.single_clicked = True
                return True
        count = len(self.legends)
        for i,l in enumerate(self.legends):
            if l.hitMe(x,y):
                l.drawSelected()
                if self.current_legend != -1:
                    self.legends[self.current_legend].redraw()
                Panel.printLeft(u"选择了第%d份快照"%(i+1))
                self.current_legend = i
                self.my_cube_3d = l
                self.single_clicked = True          
                return True
        return False
        
    def doubleClick(self):
        if self.single_clicked:
            #print("lib double clickd")
            self.single_clicked = False     
            return True
        self.single_clicked = False     
        return False