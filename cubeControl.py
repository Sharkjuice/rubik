# -*- coding: utf-8 -*-  
import pygame,sys,time,random,copy,subprocess
import cubeModel,cubeView
from cubeGlobal import cube_o,win_height,win_width,fov,distance,background,screen,black,green,bright_green,colors_r,colors_n
from cubeCommon import button,printText
from cubeTutorial import displayTutorial,nextOrPrevious

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

class CubeController:
    def __init__(self, x_offset,y_offset,init_count, his_count):
        self.x_offset =  x_offset
        self.y_offset = y_offset
        self.init_count = init_count
        self.his_actions = []
        self.auto_actions = []
        self.his_count = his_count

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
        self.brush_block = (-100,-100,-100)
        self.brush_face = -1
        self.brush_status = 0 #0: None, 1: Copy, 2:Brush

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
       
        self.my_cube_3d = cubeView.Cube3D(my_cube,win_width, win_height, fov, distance,self.x_offset,self.y_offset,0,-30)
        self.displayCube(screen)
        
        self.sn_cube_3d = cubeView.Cube3D(my_cube,500, 500, 700, 12, self.x_offset, self.y_offset,820,50)

                

    def saveCube(self,dumy):
        fo = open(".\\mycube.clp", "w", 1)
        fo.write("(defrule start-up =>\n")
        for block in self.my_cube_3d.cube.blocks:
            block_str = "(assert (blk %d %d %d %c %c %c))\n" % (block.current.x, block.current.y, block.current.z,
              block.colors[0],block.colors[1],block.colors[2])
            fo.write(block_str)
        fo.write("\n(assert (phase 0)))")
        fo.close()
    
    def loadCube(self,dumy):
        self.his_actions = []
        fo = open(".\\mycube.clp", "r",1)
        blocks = []
        if fo != None:
            for line in fo.readlines():
                b = line.strip("(\n)").split(" ")
                if b[0] == "assert" and b[1] == "(blk":
                    blocks.append(((int(b[2]),int(b[3]),int(b[4])),"".join([b[5],b[6],b[7]])))
            fo.close()
            cube = cubeModel.Cube(blocks)
            self.my_cube_3d = cubeView.Cube3D(cube,win_width, win_height, fov, distance,self.x_offset,self.y_offset,0,-30)
            self.displayCube(screen)
        
 
    def resetCube(self,dumy):
        my_cube = cubeModel.Cube()
        self.my_cube_3d = cubeView.Cube3D(my_cube,win_width, win_height, fov, distance,self.x_offset,self.y_offset,0,-30)
        self.displayCube(screen)
        self.sn_cube_3d = cubeView.Cube3D(my_cube,500, 500, 700, 12, self.x_offset, self.y_offset,820,50)
        self.his_actions = []
        

#随机生成一个初始乱的魔方
    def initCube(self,dumy):
        ra_map = ["F", "R", "U", "F'", "R'", "U'","f", "r","u","f'", "r'","u'",
          "B", "L", "D", "B'", "L'", "D'"]
        for i in range(self.init_count):
            r = int(random.random()*18)
            face = a_map[ra_map[r]]["face"]
            layer = a_map[ra_map[r]]["layer"]
            clockwize = a_map[ra_map[r]]["clockwize"]
            self.my_cube_3d.cube.rotateCube(face,layer,clockwize)
        self.displayCube(screen)        
        self.his_actions = []
        
    def displayCube(self,screen):
        self.my_cube_3d.buildFaces()        
        self.my_cube_3d.displayCube(screen)
        self.my_cube_3d.displayLayer(screen,"RIGHT",2, -120, -110)
        self.my_cube_3d.displayLayer(screen,"UP",2, -156, 295)
        self.my_cube_3d.displayLayer(screen,"FRONT",2, 360, -110)
    

    def helpCube(self,dumy):
        nextOrPrevious(0)
        pygame.draw.rect(screen,background,(self.x_offset + 810,self.y_offset + 5,538,595))
    

    def snapCube(self,dumy):       
        snapshot_cube_mode = copy.deepcopy(self.my_cube_3d.cube)
        self.sn_cube_3d.cube = snapshot_cube_mode
        self.sn_cube_3d.buildFaces()
        self.comparing = False
        pygame.draw.rect(screen,background,(self.x_offset + 810, self.y_offset + 5,538,595))    
        self.sn_cube_3d.displayCube(screen)
        self.sn_cube_3d.displayLayer(screen,"RIGHT",2, 180,-70)
        self.sn_cube_3d.displayLayer(screen,"UP",2, 160, 260)
        self.sn_cube_3d.displayLayer(screen,"FRONT",2, 480, -70)
   
    def compareCube(self,dumy):
        if self.comparing:#已经处于比对状态，先取消
            self.cancel(dumy)
        self.comparing = True        
        mark = 1
        for my_b in self.my_cube_3d.blocks:        
            for sn_b in self.sn_cube_3d.blocks:
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
            self.my_cube_3d.displayCube(screen)
            self.sn_cube_3d.displayCube(screen)
                    

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
        self.hint(dumy)
        self.auto_actions = self.parseAdvice()

    def parseAdvice(self):
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
        self.saveCube(dumy)
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
                self.my_cube_3d.displayCube(screen)
            

    def cancel(self,dumy):
        if self.brush_status != 0:
            self.brush_color = "-"
            self.brush_block = (-100,-100,-100)
            self.brush_face = -1
            self.brush_status = 0
            self.message = u"操作历史"
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.comparing = False        
            mark = 1
            for my_b in self.my_cube_3d.blocks:        
                if  my_b.mark != "-":
                    my_b.mark = "-"
            for sn_b in self.sn_cube_3d.blocks:       
                if  sn_b.mark != "-":
                    sn_b.mark = "-"
            self.my_cube_3d.displayCube(screen)
            self.sn_cube_3d.displayCube(screen)
        else:#撤销上次的转动
            self.singleRotate(None)    
        
    def detectAction(self,block,face,start,end):
        rel_y = end[1] - start[1]
        rel_x = end[0] - start[0]
        dir = "-"
        if (abs(rel_x) < 5 and abs(rel_y) < 5):
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

    def gameLoop(self):
        hit_b = ""
        hit_f = -1      
        clock = pygame.time.Clock()
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                    
                    self.gameExit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (not self.rotating):
                        mouse_down_x,mouse_down_y = event.pos
                        hit_b,hit_f = self.my_cube_3d.hitBlock(mouse_down_x,mouse_down_y)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and (not self.rotating):
                        mouse_up_x,mouse_up_y = event.pos
                        if hit_f != -1:
                            action = self.detectAction(hit_b,hit_f,
                                            (mouse_down_x,mouse_down_y),
                                            (mouse_up_x,mouse_up_y))
                            if action != "-":
                                self.singleRotate(action)
                                
                            #double click, to copy facelet color
                            self.dk_count += 1
                            if self.dk_count == 1:
                                self.dk_time = pygame.time.get_ticks()
                            if self.dk_count == 2:
                                if (pygame.time.get_ticks() - self.dk_time) < 500:
                                    self.brush_block = hit_b
                                    self.brush_face  = hit_f
                                    self.brush_status = 2
                                self.dk_time = pygame.time.get_ticks()
                            if self.dk_count == 3:
                                if (pygame.time.get_ticks() - self.dk_time) < 500:
                                    blocks = [item for item in self.my_cube_3d.blocks if item.block.current == hit_b]                                   
                                    self.brush_color = colors_r[blocks[0].colors[hit_f]]
                                    self.dk_count = 0
                                    self.brush_block = (-100, -100, -100)
                                    self.brush_face  = -1
                                    self.brush_status = 1
                                    self.message = u"开始设置方块颜色。当前颜色：" + colors_n[self.brush_color]
                                    print("Start paste, block: ",hit_b," facelet:  ", hit_f," color: ", self.brush_color)
                                self.dk_time = pygame.time.get_ticks()
                                    

            #显示控制按钮
            b_map = [["F","F'","f","f'","B","B'"],["R","R'","r","r'","L","L'",],
                     ["U","U'","u","u'","D","D'"],["x","x'","y","y'","z","z'"]]
            b_x = 810
            b_y = 610
            for bs in b_map:
                for b in bs:
                    button(screen, b, self.x_offset +  b_x, self.y_offset + b_y, 40,30,green,bright_green,self.singleRotate,b)
                    b_x += 50
                b_y += 40
                b_x = 810
            button(screen,"X",self.x_offset + 1300,y_offset + 10,40,30,green,bright_green,self.cubeQuit,"X")
            button(screen,"d",    self.x_offset + 1110,self.y_offset + 610,40,30,green,bright_green,self.singleRotate,'d')
            button(screen,"d'",    self.x_offset + 1160,self.y_offset + 610,40,30,green,bright_green,self.singleRotate,"d'")
            button(screen,u"帮助",self.x_offset + 1210,self.y_offset + 610,60,30,green,bright_green,self.helpCube,"X")  
            button(screen,u"保存",self.x_offset + 1280,self.y_offset + 610,60,30,green,bright_green,self.saveCube,"X")  


            button(screen,"M",    self.x_offset + 1110,self.y_offset + 650,40,30,green,bright_green,self.singleRotate,"M") 
            button(screen,"M'",   self.x_offset + 1160,self.y_offset + 650,40,30,green,bright_green,self.singleRotate,"M'") 


            button(screen,u"快照",self.x_offset + 1210,self.y_offset + 650,60,30,green,bright_green,self.snapCube,"X" )
            button(screen,u"加载",self.x_offset + 1280,self.y_offset + 650,60,30,green,bright_green,self.loadCube,"X")  


            button(screen,"l",    self.x_offset + 1110,self.y_offset + 690,20,30,green,bright_green,self.singleRotate,"l")
            button(screen,u"自动",self.x_offset + 1140,self.y_offset + 690,60,30,green,bright_green,self.stepOver,"X") 
            button(screen,u"对比",self.x_offset + 1210,self.y_offset + 690,60,30,green,bright_green,self.compareCube,"X") 
            button(screen,u"撤销",self.x_offset + 1280,self.y_offset + 690,60,30,green,bright_green,self.cancel,"X") 
           

            button(screen,u"打乱",self.x_offset + 1140,self.y_offset + 730,60,30,green,bright_green,self.initCube,"X")
            button(screen,u"开始",self.x_offset + 1210,self.y_offset + 730,60,30,green,bright_green,self.resetCube,"X")
            button(screen,"提示", self.x_offset + 1280,self.y_offset + 730,60,30,green,bright_green,self.hint,"X")
            displayTutorial(screen, self.x_offset, self.y_offset)

            if self.rotating:
                self.rotate_angle = self.rotate_angle + 6
                self.my_cube_3d.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize,self.rotate_angle)
                self.my_cube_3d.clearCube(screen)
                self.my_cube_3d.displayCube(screen)


            if self.rotate_angle == 90:
                self.my_cube_3d.cube.rotateCube(self.rotate_face,self.rotate_layer,self.rotate_clockwize)
                self.displayCube(screen)
                printText(screen,"U", "kaiti", 30, self.x_offset + 390, self.y_offset + 210, black)
                printText(screen,"F", "kaiti", 30, self.x_offset + 290, self.y_offset + 390, black)
                printText(screen,"R", "kaiti", 30, self.x_offset + 500, self.y_offset + 400, black)
                printText(screen,"B", "kaiti", 30, self.x_offset + 690, self.y_offset + 90, black)
                printText(screen,"L", "kaiti", 30, self.x_offset + 95, self.y_offset + 90, black)
                printText(screen,"D", "kaiti", 30, self.x_offset + 120, self.y_offset + 600, black)
                self.rotating = False
                self.rotate_angle = 0


            if not self.rotating:
                if len(self.auto_actions) > 0:
                    action = self.auto_actions.pop(0)
                    self.singleRotate(action)

            if (pygame.time.get_ticks() - self.dk_time) > 600:
                self.dk_count = 0
                
                if self.brush_status == 2:
                    self.brush_status = 0
                    if self.brush_color != "-":
                        self.message = u"开始设置方块颜色。当前颜色：" + colors_n[self.brush_color]
                        self.my_cube_3d.cube
                        model_b = [item.block for item in self.my_cube_3d.blocks if item.block.current == self.brush_block][0]                                   
                        
                        b = self.brush_block
                        if b[0] == -1 and self.brush_face == 3:
                            model_b.colors[0] = self.brush_color
                        if (b[0] == 1 and self.brush_face == 1):
                            model_b.colors[0] = self.brush_color
                        if (b[1] == -1 and self.brush_face == 5 ):
                            model_b.colors[1] = self.brush_color
                        if (b[1] == 1 and self.brush_face == 4):
                            model_b.colors[1] = self.brush_color
                        if (b[2] == -1 and self.brush_face == 0):
                            model_b.colors[2] = self.brush_color
                        if (b[2] == 1 and self.brush_face == 2):
                            model_b.colors[2] = self.brush_color
                        self.my_cube_3d.buildFaces()        
                        self.my_cube_3d.displayCube(screen)

                
            pygame.draw.rect(screen,(128,128,128),(x_offset + 220,y_offset + 690,560,30))            
            printText(screen, self.message, "kaiti", 25, self.x_offset + 230, self.y_offset + 690, background)
                    
            pygame.draw.rect(screen,(128,128,128),(x_offset + 220,y_offset + 730,560,30))            
            printText(screen, self.advise, "kaiti", 25, self.x_offset + 230, self.y_offset + 730, background)
                
           
            clock.tick(30)
            pygame.display.update()
    

        
if __name__ == "__main__":
    global screen

    #初始化pygame屏幕
    pygame.init()
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    screen.fill(background)
    pygame.display.set_caption("3D魔方教程")
    scn_width = screen.get_width()
    scn_height = screen.get_height()
    brd_width = 1350
    brd_height = 768
    x_offset = int((scn_width - brd_width)/2)
    y_offset = int((scn_height - brd_height)/2)

    pt1 = (x_offset,y_offset)# top left point
    pt2 = (x_offset + brd_width,y_offset)#top right point
    pt3 = (x_offset,y_offset + brd_height -2)#bottom left point
    pt4 = (x_offset + brd_width, y_offset + brd_height-2)
    
    
    
    pygame.draw.line(screen,(128,128,128),pt1,pt2,2)
    pygame.draw.line(screen,(128,128,128),pt2,pt4,2)
    pygame.draw.line(screen,(128,128,128),pt4,pt3,2)
    pygame.draw.line(screen,(128,128,128),pt3,pt1,2)

    
    pygame.draw.line(screen,(128,128,128),(x_offset + 800,y_offset),(x_offset + 800,y_offset + brd_height),2)
    pygame.draw.line(screen,(128,128,128),(x_offset + 800,y_offset + 600),(x_offset + brd_width,y_offset + 600),2)


    cubeController = CubeController(x_offset, y_offset,15,25)

    
    cubeController.gameLoop()
    pygame.quit()
  
