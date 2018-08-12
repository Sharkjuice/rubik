# -*- coding: utf-8 -*-  
import pygame,sys,time,copy,random,subprocess
import cubeModel,cubeView,cubeSnapshot,cubeTutorial,cubeLibrary
from cubeGlobal import mouse_status,m_map,cube_o,getDisplayParams,\
    background,black,green,gray,bright_green,colors_r,colors_n,colors
from cubeCommon import button,printText
from macroParse import parseAdvice


#显示魔方区域的高度和宽度
win_height = 768
win_width = 800
#3D显示参数
fov = 700
distance = 8
#0: init;1:bottom center ok;2:bottom edge ok;3 bottom corner ok
#4:layer 2 OK;#5:up color OK;#6:Game Over
p_map = {
"Simple":[0,1,2,3,4,5,6],
"F2CP":[0,1,2,4,5,6]
}

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
         "b":{"face":"FRONT","clockwize":1,"layer":5,"reverse":"b'"},
         "L":{"face":"RIGHT","clockwize":1,"layer":2,"reverse":"L'"},
         "l":{"face":"RIGHT","clockwize":1,"layer":5,"reverse":"l'"},
         "l'":{"face":"RIGHT","clockwize":-1,"layer":5,"reverse":"l"},
         "D":{"face":"UP","clockwize":-1,"layer":2,"reverse":"D'"},
         "B'":{"face":"FRONT","clockwize":-1,"layer":2,"reverse":"B"},
         "b'":{"face":"FRONT","clockwize":-1,"layer":5,"reverse":"b"},
         "L'":{"face":"RIGHT","clockwize":-1,"layer":2,"reverse":"L"},
         "D'":{"face":"UP","clockwize":1,"layer":2,"reverse":"D"},         
         "d":{"face":"UP","clockwize":-1,"layer":5,"reverse":"d'"},         
         "d'":{"face":"UP","clockwize":1,"layer":5,"reverse":"d"},         
         "y":{"face":"UP","clockwize":1,"layer":4,"reverse":"y'"},#整体绕U面中心轴顺转
         "y'":{"face":"UP","clockwize":-1,"layer":4,"reverse":"y"},#逆转
         "z":{"face":"FRONT","clockwize":-1,"layer":4,"reverse":"z'"},
         "z'":{"face":"FRONT","clockwize":1,"layer":4,"reverse":"z"},
         "x":{"face":"RIGHT","clockwize":-1,"layer":4,"reverse":"x'"},
         "x'":{"face":"RIGHT","clockwize":1,"layer":4,"reverse":"x"},
         "'|'":{"face":"FRONT","clockwize":1,"layer":6,"reverse":"'|'"}
}

class CubeController:
    def __init__(self, init_count, his_count,auto_level=2):
        self.init_count = init_count
        self.his_actions = []
        self.auto_actions = []
        self.his_colors = []
        self.his_count = his_count
        self.auto_level = auto_level
        self.resolve_method = "F2CP"
        self.right_panel = "library"

        #控制动画显示某一层的转动
        #是否在转动中， 用户启动转动，转动90度后自动停止
        self.rotating = False

        self.gameExit = False
        self.message = u"操作历史"
        self.advice = u"下一步提示"
        self.current_level = 0
        self.dk_count = 0
        self.dk_time = 0
        self.brush_color = "-"
        self.brush_copy  = 0 #0: not starting copy 1: in copy status
        #宏按钮分页
        self.total_page = len(m_map) - 1
        self.current_page = 0

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
        self.my_library = cubeLibrary.CubeLibrary(my_cube,500, 500, 700, 12, 820,50)
        self.my_library.selectSnapshot()

	#flag:0 保存为mycube.clp为了进行规则计算;1:保存为mycubexx.clp
    def save(self,flag=1):
        if self.right_panel != "library":
            screen,ft_sz,x_scale,y_scale= getDisplayParams()
            pygame.draw.rect(screen,background,(x_scale*810,
                y_scale*5,x_scale*538,y_scale*595))    
            self.right_panel = "library"
    
        msg = self.save2()
        self.message = msg    
        
    def save2(self,flag=1,figure=0):
        msg = self.my_library.saveCube(self.my_cube_3d.cube,flag, figure)            
        return msg        
            
    def load(self,dumy):
        self.his_actions = []
        cube = None
        if self.right_panel == "snapshot":
            cube = copy.deepcopy(self.my_snapshot.sn_cube_3d.cube)
        elif self.right_panel == "library":
            cube = copy.deepcopy(self.my_library.sn_cube_3d.cube)
        if cube != None:
            self.my_cube_3d = cubeView.Cube3D(cube,win_width, win_height, fov, 
                distance,0,-30)
            self.displayCube()
        
 
    def reset(self,dumy):
        my_cube = cubeModel.Cube()
        self.my_cube_3d = cubeView.Cube3D(my_cube,win_width, win_height, fov, 
            distance,0,-30)
        self.displayCube()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube,500, 500, 700, 12, 
            820,50)
        self.his_actions = []
        

#随机生成一个初始乱的魔方
    def init(self,init_level=0):
        self.current_level = init_level
        self.init2(init_level)
        self.his_actions = []
        self.advice = ""
        self.displayCube()   

#随机生成一个初始乱的魔方
    def init2(self,init_level):
        r_list = ["F", "R", "U", "F'", "R'", "U'","f", 
                  "r","u","f'", "r'","u'","B", "L", "D", 
                  "B'", "L'", "D'","b","b'"]
        self.stage = 0
        total = len(r_list)
        for i in range(self.init_count):
            r = int(random.random()*total)
            face = a_map[r_list[r]]["face"]
            layer = a_map[r_list[r]]["layer"]
            clockwize = a_map[r_list[r]]["clockwize"]
            self.my_cube_3d.cube.rotateCube(face,layer,clockwize)
        #rotate to F2L stage
        auto_actions = []
        init_stage = p_map[self.resolve_method][init_level]
        while self.stage < init_stage:
            for a in auto_actions:
                face = a_map[a]["face"]
                layer = a_map[a]["layer"]
                clockwize = a_map[a]["clockwize"]
                self.my_cube_3d.cube.rotateCube(face,layer,clockwize)
            advice = self.hint2()
            auto_actions = parseAdvice(advice.get("h",""))
            if auto_actions == "":
                break
#进阶到下一个阶段
    def next(self,dummy):
        self.current_level += 1
        if self.current_level >= len(p_map[self.resolve_method]):
            self.message = "魔方已经完全解决"
            return
        next_stage = p_map[self.resolve_method][self.current_level]
        auto_actions = []		
        while self.stage < next_stage:
            for a in auto_actions:
                face = a_map[a]["face"]
                layer = a_map[a]["layer"]
                clockwize = a_map[a]["clockwize"]
                self.my_cube_3d.cube.rotateCube(face,layer,clockwize)
            advice = self.hint2()
            auto_actions = parseAdvice(advice.get("h",""))
            if auto_actions == "":
                break
        self.his_actions = []
        self.advice = ""
        self.displayCube()   
        
    def displayCube(self):
        self.my_cube_3d.buildFaces()        
        self.my_cube_3d.displayCube()
        self.my_cube_3d.displayLayer("RIGHT",2, -120, -110)
        self.my_cube_3d.displayLayer("UP",2, -156, 295)
        self.my_cube_3d.displayLayer("FRONT",2, 360, -110)
    

    def help(self,dumy):
        if self.right_panel != "help":
            screen,ft_sz,x_scale,y_scale= getDisplayParams()
            pygame.draw.rect(screen,background,(x_scale*810,
                y_scale*5,x_scale*538,y_scale*595))    
            self.right_panel = "help"
            self.my_tutorial.nextOrPrevious(0)

    def snapshot(self,dumy): 
        if self.right_panel != "snapshot":
            self.right_panel = "snapshot"
            screen,ft_sz,x_scale,y_scale= getDisplayParams()
            pygame.draw.rect(screen,background,(x_scale*810,
                y_scale*5,x_scale*538,y_scale*595))    
    
        self.comparing = False
        self.my_snapshot.takeSnapshot(self.my_cube_3d.cube)
   
    def compare(self,dumy):
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
                    elif my_b.block.colors != sn_b.block.colors:
                        str_mark = str(mark)
                        my_b.mark = str_mark
                        sn_b.mark = str_mark
                        mark += 1
                        
        if mark > 1:
            self.my_cube_3d.displayCube()
            self.my_cube_3d.displayLayer("RIGHT",2, -120, -110)
            self.my_cube_3d.displayLayer("UP",2, -156, 295)
            self.my_cube_3d.displayLayer("FRONT",2, 360, -110)
            self.my_snapshot.displayCube()

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

    def macroRotate(self,macro):
        self.auto_actions = parseAdvice(macro) 
        
    def quit(self,dumy):
        self.gameExit = True

    def step(self,dumy):
        self.advice = self.hint2().get("h","")
        if self.advice != "End":
            self.auto_actions = parseAdvice(self.advice)

    def delete(self,dumy):
        if self.right_panel != "library":
            msg = u"当前是帮助窗口，不能删除."
        else:
            msg = self.my_library.deleteSnapshot()
        if msg != None:
            self.message = msg
    def hint(self,show):
        advice = self.hint2()
        print(advice)
        t1 = advice.get("t1", None)
        t2 = advice.get("t2", None)
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

    def hint2(self):
        self.save2(0)
        if self.resolve_method == "F2CP":
            res = subprocess.Popen("clipsutil.exe rubik-flcp.clp",bufsize = 1,shell = True,stdout=subprocess.PIPE)
        else:
            res = subprocess.Popen("clipsutil.exe rubik-simple.clp",bufsize = 1,shell = True,stdout=subprocess.PIPE)
        outlines = res.stdout.readlines()
        adv_p = []
        for outline in outlines:
            #print(outline)
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
        i = 0
        best = []
        while best == [] and i < 5:
            best = [ adv for adv in adv_p if adv["p"] == i ]
            i += 1
        if best == []:
            return {}
        self.advice = best[0].get("h","No Advise")
        self.stage = best[0]["s"]
        self.figure = best[0].get("f",0)
        t1 = best[0].get("t1", None)
        t2 = best[0].get("t2", None)
        #print(best[0])
        return best[0]

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
            self.cancelBrush() 
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.cancelComparing()
        else:#撤销上次的转动
            self.singleRotate(None)    
        
    def detectAction(self,block,face,start,end):
        _, _, x_scale,_ = getDisplayParams()
        motion_sz = 50*x_scale      
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
            self.my_cube_3d.displayCube()

    def endBrush(self,dumy):
        if self.brush_copy == 1:
            if not self.my_cube_3d.cube.validateCube():
                self.advice = u"颜色设置没有完成，请继续完成设置！"
                return 0
            else:
                self.brush_copy = 0
                self.advice = u"颜色设置完成。"
    def library(self,level):
        if self.right_panel != "library":
            screen,ft_sz,x_scale,y_scale= getDisplayParams()
            pygame.draw.rect(screen,background,(x_scale*810,
                y_scale*5,x_scale*538,y_scale*595))    
            self.right_panel = "library"
            self.my_library.selectSnapshot()
    def method(self,method):
        self.resolve_method = method
        self.message = "当前提示和自动解题方法是" + method

    def nextPage(self,flag):
        if self.current_page < self.total_page:
            self.current_page += 1
    def prevPage(self,flag):
        if self.current_page > 0:
            self.current_page -= 1

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
                        hit_b,hit_f = self.my_cube_3d.hitBlock(mouse_down_x,mouse_down_y)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and (not self.rotating):
                        mouse_up_x,mouse_up_y = event.pos
                        mouse_status[0] = 1
                        mouse_status[1] = mouse_up_x
                        mouse_status[2] = mouse_up_y
                        if hit_f != -1:
                            action = self.detectAction(hit_b,hit_f,
                                            (mouse_down_x,mouse_down_y),
                                            (mouse_up_x,mouse_up_y))
                            if action != "-":
                                self.singleRotate(action)
                                self.dk_count = 0
                            else:    
                                self.dk_count += 1
                                if self.dk_count == 1:
                                    self.dk_time = pygame.time.get_ticks()
                                if self.dk_count == 2:
                                    self.dk_count = 0
                                    if (pygame.time.get_ticks() - self.dk_time) < 250:
                                        if self.brush_copy == 1:
                                            self.brushColor(hit_b,hit_f)
                
            #显示宏按钮

            b_x = x_scale*10; b_y = y_scale*240; b_h = y_scale*30

            for b in m_map[self.current_page]:
                button(screen, b, ft_sz, b_x, b_y, x_scale*120,b_h,
                green,bright_green,self.macroRotate,b)
                b_y += y_scale*40;
            if self.current_page == 0:
                button(screen,"<<",ft_sz,b_x, b_y, x_scale*50,b_h,
                    gray,bright_green, self.prevPage,"X")
            else:
                button(screen,"<<",ft_sz,b_x, b_y, x_scale*50,b_h,
                    green,bright_green, self.prevPage,"X")
            if self.current_page == self.total_page:    
                button(screen,">>",ft_sz,b_x + x_scale*70, b_y, x_scale*50,b_h,
                    gray,bright_green,self.nextPage,"X")
            else:            
                button(screen,">>",ft_sz,b_x + x_scale*70, b_y, x_scale*50,b_h,
                    green,bright_green,self.nextPage,"X")
                

            #标准旋转按钮列表
            b_map = [["F","F'","f"],["f'","B","B'"],["R","R'","r"],["r'","L","L'"],
                     ["U","U'","u"],["u'","D","D'"],["x","x'","y"],["y'","z","z'"],
                     ["M","M'","l"],["d","d'","l'"],["b","b'","'|'"]]

            b_x = x_scale*650; b_y = y_scale*240; b_h = y_scale*30
            #退出按钮，最右上角
            button(screen,"X",ft_sz,x_scale*1300,y_scale*10,x_scale*40,b_h,green,bright_green,self.quit,"X")
            #显示标准旋转按钮
            for bs in b_map:
                for b in bs:
                    button(screen, b, ft_sz, b_x, b_y, x_scale*40,b_h,green,bright_green,self.singleRotate,b)
                    b_x += x_scale*50
                b_y += y_scale*40; b_x = x_scale*650
                
            #显示控制按钮
            b_map = [[(u"题库",self.library,0),
                    ("7步",self.method,"Simple"),("F2CP",self.method,"F2CP"),
                    (u"保存",self.save,1),(u"帮助",self.help,0),
                    (u"删除",self.delete,0), (u"提示",self.hint,1),
                    (u"开始",self.reset,0)],
                     [(u"<-|",self.load,0),(u"|->",self.snapshot,0),
                     (u"对比",self.compare,0),("打乱",self.init,1),
                     (u"进阶",self.next,2),(u"保留",None,0),
                     (u"自动",self.step,0),(u"撤销",self.cancel,0),
                     ]]

            b_x = x_scale*790; b_y = y_scale*690; b_h = y_scale*30
            for bs in b_map:
                for b,f,p in bs:
                    if f != None:               
                        button(screen, b, ft_sz, b_x, b_y, x_scale*60,b_h,green,bright_green,f,p)
                    else:
                        button(screen, b, ft_sz, b_x, b_y, x_scale*60,b_h,gray,bright_green,f,p)
                    b_x += x_scale*70
                b_y += y_scale*40; b_x = x_scale*790
                     
            #显示设置颜色块
            b_map = ["r","b","g","o","y","w"]
            b_x = x_scale*230; b_y = y_scale*10; b_h = y_scale*30
            for b in b_map:
                    button(screen, "", ft_sz, b_x, b_y, x_scale*40,b_h,
                        colors[b],bright_green,self.selectColor,b)
                    b_x += x_scale*50
                
            button(screen,u"完成",ft_sz, b_x, b_y, x_scale*60, b_h,
                (224,224,224),bright_green,self.endBrush,"x")
                

            if self.rotating:
                self.rotate_angle = self.rotate_angle + 6
                self.my_cube_3d.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize,self.rotate_angle)
                self.my_cube_3d.clearCube()
                self.my_cube_3d.displayCube()


            if self.rotate_angle == 90:
                self.my_cube_3d.cube.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize)
                self.displayCube()
                printText(screen,"U", "arial", ft_sz, x_scale*390, y_scale*220, black)
                printText(screen,"F", "arial", ft_sz, x_scale*290, y_scale*390, black)
                printText(screen,"R", "arial", ft_sz, x_scale*500, y_scale*400, black)
                printText(screen,"B", "arial", ft_sz, x_scale*690, y_scale*90, black)
                printText(screen,"L", "arial", ft_sz, x_scale*95, y_scale*93, black)
                printText(screen,"D", "arial", ft_sz, x_scale*120, y_scale*600, black)
                self.rotating = False
                self.rotate_angle = 0


            if not self.rotating:
                if len(self.auto_actions) > 0:
                    action = self.auto_actions.pop(0)
                    self.singleRotate(action)

                
            pygame.draw.rect(screen,(128,128,128),(x_scale*220,y_scale*690,x_scale*560,y_scale*30))            
            printText(screen, self.message, "fangsong", ft_sz, x_scale*230, y_scale*690, background)
                    
            pygame.draw.rect(screen,(128,128,128),(x_scale*220,y_scale*730,x_scale*560,y_scale*30))            
            printText(screen, self.advice, "fangsong", ft_sz, x_scale*230, y_scale*730, background)
            
            if self.right_panel == "library":
                self.my_library.displayHeader()
            elif self.right_panel == "help":
                self.my_tutorial.displayHeader()
           
            clock.tick(30)
            pygame.display.update()
    
  
