# -*- coding: utf-8 -*-  
import pygame,sys,time,copy,random,subprocess,ctypes
import cubeModel,cubeView,cubeSnapshot,cubeTutorial
from cubeGlobal import mouse_status,cube_o,setDisplayParams,getDisplayParams,\
    background,black,green,bright_green,colors_r,colors_n,colors
from cubeCommon import button,printText

#action map用户在几面上的按钮，对应的数据模型
a_map = {"F":{"face":"FRONT","clockwize":-1,"layer":0,"reverse":"F'"},
         "R":{"face":"RIGHT","clockwize":-1,"layer":0,"reverse":"R'"},
         "U":{"face":"UP","clockwize":1,"layer":0,"reverse":"U'"},
         "F'":{"face":"FRONT","clockwize":1,"layer":0,"reverse":"F"},
         "R'":{"face":"RIGHT","clockwize":1,"layer":0,"reverse":"R"},
         "U'":{"face":"UP","clockwize":-1,"layer":0,"reverse":"U"},
         "f":{"face":"FRONT","clockwize":-1,"layer":3,"reverse":"f'"},
         "r":{"face":"RIGHT","clockwize":-1,"layer":3,"reverse":"r'"},
         "M":{"face":"RIGHT","clockwize":-1,"layer":1,"reverse":"M'"},
         "u":{"face":"UP","clockwize":1,"layer":3,"reverse":"u'"},
         "f'":{"face":"FRONT","clockwize":1,"layer":3,"reverse":"f"},
         "M'":{"face":"RIGHT","clockwize":1,"layer":1,"reverse":"M"},
         "r'":{"face":"RIGHT","clockwize":1,"layer":3,"reverse":"r"},
         "u'":{"face":"UP","clockwize":-1,"layer":3,"reverse":"u"},
         "B":{"face":"FRONT","clockwize":1,"layer":2,"reverse":"B'"},
         "L":{"face":"RIGHT","clockwize":1,"layer":2,"reverse":"L'"},
         "l":{"face":"RIGHT","clockwize":1,"layer":5,"reverse":"l'"},
         "l'":{"face":"RIGHT","clockwize":-1,"layer":5,"reverse":"l"},
         "D":{"face":"UP","clockwize":-1,"layer":2,"reverse":"D'"},
         "B'":{"face":"FRONT","clockwize":-1,"layer":2,"reverse":"B"},
         "L'":{"face":"RIGHT","clockwize":-1,"layer":2,"reverse":"L"},
         "D'":{"face":"UP","clockwize":1,"layer":2,"reverse":"D"},         
         "d":{"face":"UP","clockwize":-1,"layer":5,"reverse":"d'"},         
         "d'":{"face":"UP","clockwize":1,"layer":5,"reverse":"d"},         
         "y":{"face":"UP","clockwize":1,"layer":4,"reverse":"y'"},#整体绕U面中心轴顺转
         "y'":{"face":"UP","clockwize":-1,"layer":4,"reverse":"y"},#逆转
         "z":{"face":"FRONT","clockwize":-1,"layer":4,"reverse":"z'"},
         "z'":{"face":"FRONT","clockwize":1,"layer":4,"reverse":"z"},
         "x":{"face":"RIGHT","clockwize":-1,"layer":4,"reverse":"x'"},
         "x'":{"face":"RIGHT","clockwize":1,"layer":4,"reverse":"x"}
}
#显示魔方区域的高度和宽度
win_height = 768
win_width = 800
#3D显示参数
fov = 700
distance = 8
#屏幕的最小宽度和高度
min_scn_w = 1350
min_scn_h = 768

class CubeController:
    def __init__(self, init_count, his_count):
        self.init_count = init_count
        self.his_actions = []
        self.auto_actions = []
        self.his_colors = []
        self.his_count = his_count
        
        self.snapshot_or_tutorial = 0; #0 表示显示tutorial， 1表示显示snapshot

        #控制动画显示某一层的转动
        #是否在转动中， 用户启动转动，转动90度后自动停止
        self.rotating = False

        self.gameExit = False
        self.message = u"操作历史"
        self.advise = u"下一步提示"
        self.stage = 0
        self.dk_count = 0
        self.dk_time = 0
        self.brush_color = "-"
        self.brush_copy  = 0 #0: not starting copy 1: in copy status

        #转动哪一面
        self.rotate_face = ""
        #转动上述面的哪一层
        self.rotate_layer = 0
        #转动角度，开始为0，在game_loop循环中增加
        self.rotate_angle = 0
        #转动的方向，顺时针、逆时针
        self.rotate_clockwize = 1
        self.comparing = False
        #初始化数据模型
        my_cube = cubeModel.Cube()
       
        self.my_cube_3d = cubeView.Cube3D(my_cube,win_width, win_height, fov, distance,0,-30)
        self.displayCube()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube,500, 500, 700, 12, 820,50)
        self.my_tutorial = cubeTutorial.CubeTutorial()       
        self.my_tutorial.nextOrPrevious(-1)
        
    #flag:0 保存为mycube.clp为了进行规则计算;1:保存为mycubexx.clp
    def saveCube(self,flag):
        self.my_snapshot.saveCube(self.my_cube_3d.cube,flag)            

        if flag == 1:
            self.message = u"保存为第" + str(self.my_snapshot.getTotal()) + "份魔方"    
            self.snapshot_or_tutorial = 1
            #self.my_snapshot.displayCube()		

    def loadCube(self,dumy):
        self.his_actions = []
        cube = copy.deepcopy(self.my_snapshot.sn_cube_3d.cube)
        self.my_cube_3d = cubeView.Cube3D(cube,win_width, win_height, fov, 
			distance,0,-30)
        self.displayCube()
        
 
    def resetCube(self,dumy):
        my_cube = cubeModel.Cube()
        self.my_cube_3d = cubeView.Cube3D(my_cube,win_width, win_height, fov, 
            distance,0,-30)
        self.displayCube()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube,500, 500, 700, 12, 
            820,50)
        self.his_actions = []
        

#随机生成一个初始乱的魔方
    def initCube(self,dumy):
        ra_map = ["F", "R", "U", "F'", "R'", "U'","f", "r","u","f'", "r'","u'",
          "B", "L", "D", "B'", "L'", "D'"]
        self.stage = 0
        for i in range(self.init_count):
            r = int(random.random()*18)
            face = a_map[ra_map[r]]["face"]
            layer = a_map[ra_map[r]]["layer"]
            clockwize = a_map[ra_map[r]]["clockwize"]
            self.my_cube_3d.cube.rotateCube(face,layer,clockwize)

        #rotate to F2L stage
        auto_actions = []
        while self.stage < 2:
            for a in auto_actions:
                face = a_map[a]["face"]
                layer = a_map[a]["layer"]
                clockwize = a_map[a]["clockwize"]
                self.my_cube_3d.cube.rotateCube(face,layer,clockwize)
            self.advise = ""
            self.hint(dumy)
            auto_actions = self.parseAdvice()
                
        self.his_actions = []
        self.advise = ""
        self.displayCube()        
        
    def displayCube(self):
        self.my_cube_3d.buildFaces()        
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLayer("RIGHT",2, -120, -110)
        self.my_cube_3d.displayLayer("UP",2, -156, 295)
        self.my_cube_3d.displayLayer("FRONT",2, 360, -110)
    

    def helpCube(self,dumy):
        self.snapshot_or_tutorial = 0            
        self.my_tutorial.nextOrPrevious(0)
        #self.my_tutorial.displayHeader()
        #self.my_tutorial.displayTutorial()

    def snapCube(self,dumy): 
        pygame.draw.rect(screen,background,(x_scale*810,
            y_scale*5,x_scale*538,y_scale*595))    
        self.snapshot_or_tutorial = 1
        self.comparing = False
        self.my_snapshot.takeSnapshot(self.my_cube_3d.cube)
        #self.my_snapshot.displayHeader()
        #self.my_snapshot.displayCube()
   
    def compareCube(self,dumy):
        if self.comparing:#已经处于比对状态，先取消
            self.cancel(dumy)
        self.comparing = True        
        mark = 1
        sn_cube_3d = self.my_snapshot.sn_cube_3d
        for my_b in self.my_cube_3d.blocks:        
            for sn_b in sn_cube_3d.blocks:
                if my_b.block.origin == sn_b.block.origin:
                    if  my_b.block.current != sn_b.block.current:
                        str_mark = str(mark)
                        my_b.mark = str_mark
                        sn_b.mark = str_mark
                        mark += 1
                    elif my_b.block.colors[0] != sn_b.block.colors[0]:
                        str_mark = str(mark)
                        my_b.mark = str_mark
                        sn_b.mark = str_mark
                        mark += 1
                        
        if mark > 1:
            self.my_cube_3d.displayCube()
            sn_cube_3d.displayCube()
                    

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
        self.message = "".join(self.his_actions)
        return True
    
    def cubeQuit(self,dumy):
        self.gameExit = True

    def stepOver(self,dumy):
        self.advise = ""
        self.hint(dumy)
        self.auto_actions = self.parseAdvice()

    def parseAdvice(self):
        if self.advise == "":
            return ""
        macro = self.advise
        l = len(macro)
        if l == 0 : return
        ci = l-1
        pass1 = []
        while ci >= 0:
            a = macro[ci]
            if a == "'":
                ci -= 1
                pass1.insert(0,macro[ci] + a)
                ci -= 1            
            else:
                ci -= 1            
                pass1.insert(0,a)
                
        si = 0
        l = len(pass1)
        pass2 = []
        tmp = []
        ci = 0
        while ci < l:
            a = pass1[ci]
            if a == "(" :
                ci += 1
                si = ci
            elif a == ")":
                #pass2.extend(pass1[si:ci])
                tmp = pass1[si:ci]
                ci += 1
            elif a == "2":
                pass2.extend(tmp)
                ci += 1
            else:
                pass2.append(a)
                tmp = [a]
                ci += 1
                
        return pass2

    def hint(self,dumy):
        self.saveCube(0)
        res = subprocess.Popen("clipsutil.exe",bufsize = 1,shell = True,stdout=subprocess.PIPE)
        
        outlines = res.stdout.readlines()
        adv_p = []
        for outline in outlines:
            outline_str = outline.decode().strip()
            if outline_str != "" and outline_str[0] != "#":
                adv_l = outline_str.split(";")
                adv_m = {}
                for item in adv_l:
                    item1 = item.split(":")
                    adv_v = {"s":lambda x:int(x),
                             "f":lambda x:int(x),
                             "p":lambda x:int(x),
                             "h":lambda x:x,
                             "t1":lambda x: x.strip("()").split(" "),
                             "t2":lambda x: x.strip("()").split(" ")}
                    val = adv_v[item1[0]](item1[1])
                    adv_m[item1[0]] = val
                adv_p.append(adv_m)
        best = [ adv for adv in adv_p if adv["p"] == 0 ]
        if best == []:
            best = [ adv for adv in adv_p if adv["p"] == 1 ]
        if best == []:
            best = [ adv for adv in adv_p if adv["p"] == 2 ]
        if best == []:
            best = [ adv for adv in adv_p if adv["p"] == 3 ]
        if best != []:
            self.advise = best[0]["h"]
            self.stage = best[0]["s"]
            t1 = best[0].get("t1", None)
            t2 = best[0].get("t2", None)
            for my_b in self.my_cube_3d.blocks:
                if t1 != None:
                    if (my_b.block.current.x == int(t1[0]) and
                        my_b.block.current.y == int(t1[1]) and my_b.block.current.z == int(t1[2])):
                            my_b.mark = "1"
                if t2 != None:
                    if (my_b.block.current.x == int(t2[0]) and my_b.block.current.y == int(t2[1]) and
                       my_b.block.current.z == int(t2[2])):
                            my_b.mark = "2"
            if t1 != None:
                self.my_cube_3d.displayCube()
            
    def cancelComparing(self): 
        self.comparing = False        
        mark = 1
        sn_cube_3d = self.my_snapshot.sn_cube_3d        
        for my_b in self.my_cube_3d.blocks:        
            if  my_b.mark != "-":
                my_b.mark = "-"
        for sn_b in sn_cube_3d.blocks:       
            if  sn_b.mark != "-":
                sn_b.mark = "-"
        self.my_cube_3d.displayCube()
        sn_cube_3d.displayCube()


    def cancelBrush(self):
        if len(self.his_colors) > 0:
            b,i,c = self.his_colors.pop(-1)
            b.colors[i] = c
            self.my_cube_3d.buildFaces()        
            self.my_cube_3d.displayCube()
        else:
            self.brush_copy = 0
            self.message = u"取消全部设置。"
            
    def cancel(self,dumy):
        if self.brush_copy == 1:
            #print(self.his_colors)
            self.cancelBrush() 
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.cancelComparing()
        else:#撤销上次的转动
            self.singleRotate(None)    
        
    def detectAction(self,block,face,start,end):
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
        return cube_o[block][1][face].get(dir,"-")
        
    def selectColor(self,c):
        self.brush_color = c
        self.brush_copy = 1
        self.message = u"选择色块，双击魔方设置颜色。当前选中:" + colors_n[self.brush_color]

    def brushColor(self,b,f):
        if self.brush_color != "-":
            model_b = [item.block for item in self.my_cube_3d.blocks if item.block.current == b][0]                                   
            
            if b[0] == -1 and f == 3:
                self.his_colors.append((model_b,0,model_b.colors[0]))
                model_b.colors[0] = self.brush_color
            if (b[0] == 1 and f == 1):
                self.his_colors.append((model_b,0,model_b.colors[0]))
                model_b.colors[0] = self.brush_color
            if (b[1] == -1 and self.brush_face == 5 ):
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
            self.my_cube_3d.displayCube(screen)

    def endBrush(self,dumy):
        if self.brush_copy == 1:
            if not self.my_cube_3d.cube.validateCube():
                self.advise = u"颜色设置没有完成，请继续完成设置！"
                return 0
            else:
                self.brush_copy = 0
                self.advise = u"颜色设置完成。"                

    def gameLoop(self):
        global mouse_status
        hit_b = ""
        hit_f = -1      
        clock = pygame.time.Clock()
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                    
                    self.gameExit = True
                if event.type == pygame.KEYDOWN:                    
                    if event.key == pygame.K_DELETE:
                        self.my_snapshot.deleteSnapshot(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (not self.rotating):
                        mouse_down_x,mouse_down_y = event.pos
                        mouse_status[0] = 0
                        mouse_status[1] = mouse_down_x
                        mouse_status[2] = mouse_down_y
                        #print("mouse pressed, ", mouse_status)
                        hit_b,hit_f = self.my_cube_3d.hitBlock(mouse_down_x,mouse_down_y)
                        #print("hit block:",hit_b, " hit face:", hit_f)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and (not self.rotating):
                        mouse_up_x,mouse_up_y = event.pos
                        mouse_status[0] = 1
                        mouse_status[1] = mouse_up_x
                        mouse_status[2] = mouse_up_y
                        #print("mouse released, ", mouse_status)
                        if hit_f != -1:
                            action = self.detectAction(hit_b,hit_f,
                                            (mouse_down_x,mouse_down_y),
                                            (mouse_up_x,mouse_up_y))
                            if action != "-":
                                self.singleRotate(action)
                                self.dk_count = 0
                            else:    
                                #double click, to copy facelet color
                                self.dk_count += 1
                                if self.dk_count == 1:
                                    self.dk_time = pygame.time.get_ticks()
                                if self.dk_count == 2:
                                    self.dk_count = 0
                                    if (pygame.time.get_ticks() - self.dk_time) < 250:
                                        if self.brush_copy == 1:
                                            self.brushColor(hit_b,hit_f)
                
                                    

            #显示控制按钮
            b_map = [["F","F'","f","f'","B","B'"],["R","R'","r","r'","L","L'",],
                     ["U","U'","u","u'","D","D'"],["x","x'","y","y'","z","z'"]]
            b_x = x_scale*810
            b_y = y_scale*610
            b_h = y_scale*30
            for bs in b_map:
                for b in bs:
                    button(screen, b, ft_sz, b_x, b_y, x_scale*40,b_h,green,bright_green,self.singleRotate,b)
                    b_x += x_scale*50
                b_y += y_scale*40
                b_x = x_scale*810
            button(screen,"X",ft_sz,x_scale*1300,y_scale*10,x_scale*40,b_h,green,bright_green,self.cubeQuit,"X")
            button(screen,"d",ft_sz,x_scale*1110,y_scale*610,x_scale*40,b_h,green,bright_green,self.singleRotate,'d')
            button(screen,"d'",ft_sz,x_scale*1160,y_scale*610,x_scale*40,b_h,green,bright_green,self.singleRotate,"d'")
            button(screen,u"帮助",ft_sz,x_scale*1210,y_scale*610,x_scale*60,b_h,green,bright_green,self.helpCube,"X")  
            button(screen,u"保存",ft_sz,x_scale*1280,y_scale*610,x_scale*60,b_h,green,bright_green,self.saveCube,1)  
            button(screen,"M",ft_sz,x_scale*1110,y_scale*650,x_scale*40,b_h,green,bright_green,self.singleRotate,"M") 
            button(screen,"M'",ft_sz,x_scale*1160,y_scale*650,x_scale*40,b_h,green,bright_green,self.singleRotate,"M'") 
            button(screen,u"快照",ft_sz,x_scale*1210,y_scale*650,x_scale*60,b_h,green,bright_green,self.snapCube,"X" )
            button(screen,u"加载",ft_sz,x_scale*1280,y_scale*650,x_scale*60,b_h,green,bright_green,self.loadCube,"X")  
            button(screen,"l",ft_sz,x_scale*1110,y_scale*690,x_scale*20,b_h,green,bright_green,self.singleRotate,"l")
            button(screen,u"自动",ft_sz,x_scale*1140,y_scale*690,x_scale*60,b_h,green,bright_green,self.stepOver,"X") 
            button(screen,u"对比",ft_sz,x_scale*1210,y_scale*690,x_scale*60,b_h,green,bright_green,self.compareCube,"X") 
            button(screen,u"撤销",ft_sz,x_scale*1280,y_scale*690,x_scale*60,b_h,green,bright_green,self.cancel,"X")
            button(screen,"l'",ft_sz,x_scale*1110,y_scale*730,x_scale*20,b_h,green,bright_green,self.singleRotate,"l'")
            button(screen,u"打乱",ft_sz,x_scale*1140,y_scale*730,x_scale*60,b_h,green,bright_green,self.initCube,"X")
            button(screen,u"开始",ft_sz,x_scale*1210,y_scale*730,x_scale*60,b_h,green,bright_green,self.resetCube,"X")
            button(screen,"提示",ft_sz,x_scale*1280,y_scale*730,x_scale*60,b_h,green,bright_green,self.hint,"X")
            #显示设置颜色块
            button(screen,"",ft_sz,x_scale*230,y_scale*10,x_scale*40,x_scale*40,
                colors["r"],bright_green,self.selectColor,"r")
            button(screen,"",ft_sz,x_scale*280,y_scale*10,x_scale*40,x_scale*40,
                colors["b"],bright_green,self.selectColor,"b")
            button(screen,"",ft_sz,x_scale*330,y_scale*10,x_scale*40,x_scale*40,
                colors["g"],bright_green,self.selectColor,"g")
            button(screen,"",ft_sz,x_scale*380,y_scale*10,x_scale*40,x_scale*40,
                colors["o"],bright_green,self.selectColor,"o")
            button(screen,"",ft_sz,x_scale*430,y_scale*10,x_scale*40,x_scale*40,
                colors["y"],bright_green,self.selectColor,"y")
            button(screen,"",ft_sz,x_scale*480,y_scale*10,x_scale*40,x_scale*40,
                colors["w"],bright_green,self.selectColor,"w")
            button(screen,u"完成",ft_sz,x_scale*530,y_scale*10,x_scale*50,x_scale*40,
                (224,224,224),bright_green,self.endBrush,"x")
                

            if self.rotating:
                self.rotate_angle = self.rotate_angle + 6
                self.my_cube_3d.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize,self.rotate_angle)
                self.my_cube_3d.clearCube()
                self.my_cube_3d.displayCube()


            if self.rotate_angle == 90:
                self.my_cube_3d.cube.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize)
                self.displayCube()
                printText(screen,"U", "kaiti", ft_sz, x_scale*390, y_scale*220, black)
                printText(screen,"F", "kaiti", ft_sz, x_scale*290, y_scale*390, black)
                printText(screen,"R", "kaiti", ft_sz, x_scale*500, y_scale*400, black)
                printText(screen,"B", "kaiti", ft_sz, x_scale*690, y_scale*90, black)
                printText(screen,"L", "kaiti", ft_sz, x_scale*95, y_scale*93, black)
                printText(screen,"D", "kaiti", ft_sz, x_scale*120, y_scale*600, black)
                self.rotating = False
                self.rotate_angle = 0


            if not self.rotating:
                if len(self.auto_actions) > 0:
                    action = self.auto_actions.pop(0)
                    self.singleRotate(action)

                
            pygame.draw.rect(screen,(128,128,128),(x_scale*220,y_scale*690,x_scale*560,y_scale*30))            
            printText(screen, self.message, "kaiti", ft_sz, x_scale*230, y_scale*690, background)
                    
            pygame.draw.rect(screen,(128,128,128),(x_scale*220,y_scale*730,x_scale*560,y_scale*30))            
            printText(screen, self.advise, "kaiti", ft_sz, x_scale*230, y_scale*730, background)
            
            if self.snapshot_or_tutorial == 1:
                self.my_snapshot.displayHeader()
            else:
                self.my_tutorial.displayHeader()
           
            clock.tick(30)
            pygame.display.update()
    

        
if __name__ == "__main__":
    #初始化pygame屏幕
    pygame.init()
    ctypes.windll.user32.SetProcessDPIAware()
    scn_w, scn_h = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
    screen = pygame.display.set_mode((scn_w, scn_h),pygame.FULLSCREEN)
    screen.fill(background)
    pygame.display.set_caption("3D魔方教程")
    x_scale = scn_w/min_scn_w
    y_scale = scn_h/min_scn_h
    ft_sz = int(x_scale*25)
    motion_sz = 50*x_scale
    setDisplayParams(screen,25,x_scale,y_scale)    
    pt1 = (0,0)# top left point
    pt2 = (scn_w-2,0)#top right point
    pt3 = (0, scn_h-2)#bottom left point
    pt4 = (scn_w-2, scn_h-2)
    
    pygame.draw.line(screen,(128,128,128),pt1,pt2,2)
    pygame.draw.line(screen,(128,128,128),pt2,pt4,2)
    pygame.draw.line(screen,(128,128,128),pt4,pt3,2)
    pygame.draw.line(screen,(128,128,128),pt3,pt1,2)
    
    pygame.draw.line(screen,(128,128,128),(x_scale*800,0),(x_scale*800,scn_h-2),2)
    pygame.draw.line(screen,(128,128,128),(x_scale*800,y_scale*600),(scn_w-2,y_scale*600),2)

    cubeController = CubeController(15,25)
    
    cubeController.gameLoop()
    pygame.quit()
  
