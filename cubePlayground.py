# -*- coding: utf-8 -*-  
import pygame,time,copy
import cubeModel,cubeAnimation
from cubeGlobal import mouse_status,m_map,a_map,cube_o,\
    black,green,white,red,colors_r,colors_n,colors
from cubeCommon import button,printText
from macroParse import parseAdvice
from cubePanel import Panel

#显示魔方区域的高度和宽度
height = 768
width = 800
#3D显示参数
fov = 700
distance = 8
adj_xy = (-10, -40)
his_count = 20
#x,y坐标，在各面中心打印字母
s_map = [['U',(380,210),(1, 1)], ['R',(490,380),(2, -1)],
         ['F',(280,380),(0,-1)], ['B',(685,85), (0, 1)],
         ['L',(90,90),  (2,1)], ['D',(115,605),(1,-1)]
        ]

class CubePlayground:
    def __init__(self, my_cube):
        self.his_actions = []
        self.his_count = his_count
        self.auto_actions = []
        self.his_colors = []
        #控制动画显示某一层的转动
        #是否在转动中， 用户启动转动，转动90度后自动停止
        self.brush_color = "-"
        self.brush_copy  = 0 #0: not starting copy 1: in copy status
        #宏按钮分页
        self.total_page = len(m_map) - 1
        self.current_page = 0
        #控制动画显示某一层的转动
        #是否在转动中， 用户启动转动，转动90度后自动停止
        self.rotating = False       
        #转动哪一面
        self.rotate_face = ""
        #转动上述面的哪一层
        self.rotate_layer = 0
        #转动角度，开始为0，在game_loop循环中增加
        self.rotate_angle = 0
        #转动的方向，顺时针、逆时针
        self.rotate_clockwize = 1
        #鼠标点击状态
        self.click_block = (-2,-2,-2)
        self.click_face = -1

        #初始化数据模型
        self.my_cube_3d = cubeAnimation.CubeAnimation(my_cube,width, 
                      height, fov, distance,adj_xy[0],adj_xy[1])
        self.my_cube_3d.buildFaces()
        self.my_cube_3d.setLBDPos([(-120, -110),(360, -110),
                                                (-150, 305)])
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLBD()
        self.displayCenterText()

    def displayContent(self):
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLBD()
        self.displayCenterText()
    
    def displayCenterText(self):
        screen,ft_sz,x_scale,y_scale= Panel.screen, \
             Panel.ft_sz,Panel.x_scale,Panel.y_scale
        center = [(b.current.x,b.current.y,b.current.z,b.colors)
            for b in self.my_cube_3d.cube.blocks if 
            abs(b.current.x)+abs(b.current.y)+abs(b.current.z) == 1]
        
        for s in s_map:
            c = [[c for c in x[3] if c != "-"] for x in center if x[s[2][0]] == s[2][1]][0][0]
            if c == "b":
                printText(screen,s[0], "arial", ft_sz, x_scale*s[1][0], y_scale*s[1][1], white)
            else:
                printText(screen,s[0], "arial", ft_sz, x_scale*s[1][0], y_scale*s[1][1], black)
    
    def singleRotate(self,action):
        reverse = False
        if self.rotating:
            return False
        if action == None:
            if len(self.his_actions) > 0:
                pre_action = self.his_actions.pop(-1)
                pre_action_info = a_map.get(pre_action)
                action = pre_action_info["reverse"]
                reverse = True
        if action != None:
            self.rotate_layer = a_map[action]["layer"]
            self.rotating = True
            self.rotate_angle = 0
            self.rotate_face = a_map[action]["face"]
            self.rotate_layer = a_map[action]["layer"]
            self.rotate_clockwize = a_map[action]["clockwize"]
            if not reverse:
                if len(self.his_actions) < self.his_count:
                    self.his_actions.append(action)
                else:
                    self.his_actions.pop(0)
                    self.his_actions.append(action)
        msg = "".join(self.his_actions)
        Panel.printLeft(msg)
        return True

    def macroRotate(self,macro):
        self.auto_actions = parseAdvice(macro) 
        
    def cancelBrush(self):
        if len(self.his_colors) > 0:
            b,i,c = self.his_colors.pop(-1)
            b.colors[i] = c
            self.my_cube_3d.buildFaces()        
            self.my_cube_3d.displayCube()
        else:
            self.brush_copy = 0
            Panel.printLeft(u"取消全部设置")
        
    def cancel(self,dumy):
        if self.brush_copy == 1:
            self.cancelBrush() 
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.cancelComparing()
        else:#撤销上次的转动
            self.singleRotate(None)    
        
    def detectAction(self,start,end):
        motion_sz = 50*Panel.x_scale      
        rel_y = end[1] - start[1]
        rel_x = end[0] - start[0]
        dir = "-"
        if (abs(rel_x) < motion_sz and abs(rel_y) < motion_sz):
            return dir
        
        if rel_x == 0:
            rel_x = 1
        slop = rel_y/(rel_x*1.0)
        if abs(slop) > 0.86:
            if rel_y < 0:
                dir = "U"
            else:
                dir = "D"        
        if slop > 0 and slop < 0.8:
            if rel_x > 0:
                dir = "Rd"
            else:
                dir = "Lu"
        if slop < 0 and slop > -0.8:
            if rel_x > 0:
                dir = "Ru"
            else:
                dir = "Ld"
        return cube_o[self.click_block][1][self.click_face].get(dir,"-")
        
    def selectColor(self,c):
        self.brush_color = c
        self.brush_copy = 1
        Panel.printLeft(u"选择色块，双击魔方设置颜色。当前选中:" 
                                   + colors_n[self.brush_color])

    def brushColor(self):
        b = self.click_block
        f = self.click_face
        if self.brush_color != "-":
            model_b = [item.block for item in self.my_cube_3d.blocks if item.block.current == b][0]                                   
            
            if b[0] == -1 and f == 3:
                self.his_colors.append((model_b,0,model_b.colors[0]))
                model_b.colors[0] = self.brush_color
            if (b[0] == 1 and f == 1):
                self.his_colors.append((model_b,0,model_b.colors[0]))
                model_b.colors[0] = self.brush_color
            if (b[1] == -1 and f == 5 ):
                self.his_colors.append((model_b,1,model_b.colors[1]))
                model_b.colors[1] = self.brush_color
            if (b[1] == 1 and f == 4):
                self.his_colors.append((model_b,1,model_b.colors[1]))
                model_b.colors[1] = self.brush_color
            if (b[2] == -1 and f == 0):
                self.his_colors.append((model_b,2,model_b.colors[2]))
                model_b.colors[2] = self.brush_color
            if (b[2] == 1 and f == 2):
                self.his_colors.append((model_b,2,model_b.colors[2]))
                model_b.colors[2] = self.brush_color
            
            self.my_cube_3d.buildFaces()        
            self.my_cube_3d.displayCube()

    def endBrush(self,dumy):
        if self.brush_copy == 1:
            if not self.my_cube_3d.cube.validateCube():
                msg = u"颜色设置没有完成，请继续完成设置！"
            else:
                self.brush_copy = 0
                msg = u"颜色设置完成"
            Panel.printLeft(msg)
                
    def nextPage(self,flag):
        if self.current_page < self.total_page:
            self.current_page += 1
    def prevPage(self,flag):
        if self.current_page > 0:
            self.current_page -= 1
    
    def displayRotation(self):
        if self.rotating:
            self.rotate_angle = self.rotate_angle + 10
            self.my_cube_3d.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize,self.rotate_angle)
            self.my_cube_3d.clearCube()
            self.my_cube_3d.displayCube()

        if self.rotate_angle == 90:
            self.cube().rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize)
            self.rebuild()
            self.my_cube_3d.displayCube()
            self.my_cube_3d.displayLBD()
            self.displayCenterText()            
            self.rotating = False
            self.rotate_angle = 0

        if not self.rotating:
            if len(self.auto_actions) > 0:
                action = self.auto_actions.pop(0)
                self.singleRotate(action)
    
    def displayHeader(self):
        screen,ft_sz,x_scale,y_scale= Panel.screen, \
             Panel.ft_sz,Panel.x_scale,Panel.y_scale

        #显示宏按钮
        b_x = x_scale*10; b_y = y_scale*240; b_h = y_scale*30

        for b in m_map[self.current_page]:
            button(screen, b, ft_sz, b_x, b_y, x_scale*120,b_h,
            green,red,self.macroRotate,b)
            b_y += y_scale*40;
        if self.current_page == 0:
            button(screen,"<<",ft_sz,b_x, b_y, x_scale*50,b_h,
                Panel.gray,red, self.prevPage,"X")
        else:
            button(screen,"<<",ft_sz,b_x, b_y, x_scale*50,b_h,
                green,red, self.prevPage,"X")
        if self.current_page == self.total_page:    
            button(screen,">>",ft_sz,b_x + x_scale*70, b_y, x_scale*50,b_h,
                Panel.gray,red,self.nextPage,"X")
        else:            
            button(screen,">>",ft_sz,b_x + x_scale*70, b_y, x_scale*50,b_h,
                green,red,self.nextPage,"X")
            

        #标准旋转按钮列表
        b_map = [["F","F'","f"],["f'","B","B'"],["R","R'","r"],["r'","L","L'"],
                 ["U","U'","u"],["u'","D","D'"],["x","x'","y"],["y'","z","z'"],
                 ["M","M'","l"],["d","d'","l'"],["b","b'","'|'"]]

        b_x = x_scale*660; b_y = y_scale*240; b_h = y_scale*30
        #显示标准旋转按钮
        for bs in b_map:
            for b in bs:
                button(screen, b, ft_sz, b_x, b_y, x_scale*40,b_h,green,red,self.singleRotate,b)
                b_x += x_scale*50
            b_y += y_scale*40; b_x = x_scale*660
                     
        #显示设置颜色块
        b_map = ["r","b","g","o","y","w"]
        b_x = x_scale*230; b_y = y_scale*10; b_h = y_scale*30
        for b in b_map:
            button(screen, "", ft_sz, b_x, b_y, x_scale*40,b_h,                
                              colors[b],red,self.selectColor,b)
            b_x += x_scale*50
            
        button(screen,u"完成",ft_sz, b_x, b_y, x_scale*60, b_h,
            (224,224,224),red,self.endBrush,"x")
                
    def singleClick(self,x,y):
        self.click_block,self.click_face = self.my_cube_3d.hitBlock(x,y)
        if self.click_face == -1:
            return False
        return True
        
    def doubleClick(self):
        if self.brush_copy == 1:
            self.brushColor()
            return True
        return False
        
    def drag(self,xy1,xy2):
        if self.click_face != -1:
            action = self.detectAction(xy1,xy2)
            if action != "-":
                self.singleRotate(action)
                return True
        return False
        
  
    def cube(self):
        return self.my_cube_3d.cube 
   
    def load(self,cube):
        self.his_actions = []
        self.my_cube_3d.cube = copy.deepcopy(cube) 

    def blocks(self):
        return self.my_cube_3d.blocks

    def rebuild(self):
        return self.my_cube_3d.buildFaces()
        