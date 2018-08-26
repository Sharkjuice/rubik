# -*- coding: utf-8 -*-  
import pygame,sys,time,copy,random,subprocess,math
import cubeModel,cubeView,cubeSnapshot,cubeTutorial,\
        cubeLibrary,cubePlayground
from cubeGlobal import mouse_status,m_map,a_map,cube_o,\
        getDisplayParams,background,black,green,gray,\
        red,colors_r,colors_n,colors
from cubeCommon import button,printText,printLeft,\
    printHint,printRight
from macroParse import parseAdvice

#0: init;1:bottom center ok;2:bottom edge ok;3 bottom corner ok
#4:layer 2 OK;#5:up color OK;#6:Game Over
p_map = {
"Simple":[0,1,2,3,4,5,6],
"F2CP":[0,1,2,4,5,6]
}

def clearRight():
    screen,ft_sz,x_scale,y_scale= getDisplayParams()
    right_x = x_scale*822
    right_y = y_scale*5
    right_w = x_scale*528
    right_h = y_scale*675
    pygame.draw.rect(screen,background,rightPanelRect())    

class CubeControl:
    def __init__(self, init_count, his_count,auto_level=2):
        self.init_count = init_count
        self.resolve_method = "F2CP"
        self.right_panel = "library"

        self.gameExit = False
        self.current_level = -1
        self.dk_count = 0
        self.dk_time = 0

        self.comparing = False
        #初始化数据模型
        my_cube = cubeModel.Cube()
       
        self.my_playground = cubePlayground.CubePlayground(my_cube)
        self.my_playground.displayCube()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube)
        self.my_tutorial = cubeTutorial.CubeTutorial()       
        self.my_library = cubeLibrary.CubeLibrary(my_cube)
        self.my_library.selectSnapshot()
        printLeft(u"当前解题方法是" + self.resolve_method + u"法")
        printHint(u"下一步提示")

    def clearRight(self):
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        right_x = x_scale*820
        right_y = y_scale*5
        right_w = x_scale*528
        right_h = y_scale*675
        pygame.draw.rect(screen,background,
			(right_x,right_y,right_w,right_h))    
    #flag:0 保存为mycube.clp为了进行规则计算;1:保存为mycubexx.clp
    def save(self,flag=1):
        if self.right_panel != "library":
            self.clearRight() 
            self.right_panel = "library"
    
        self.save2()
        
    def save2(self,flag=1,figure=0):
        self.my_library.saveCube(self.my_playground.cube(),
            flag, figure)            
            
    def load(self,dumy):
        self.his_actions = []
        cube = None
        if self.right_panel == "snapshot":
            cube = copy.deepcopy(self.my_snapshot.cube())
        elif self.right_panel == "library":
            cube = copy.deepcopy(self.my_library.cube())
        if cube != None:
            self.my_playground.my_cube_3d.cube = cube
            self.my_playground.rebuild()            
            self.my_playground.displayCube()
        
 
    def reset(self,dumy):
        my_cube = cubeModel.Cube()
        self.my_playground = cubePlayground.CubePlayground(my_cube) 
        self.my_playground.displayCube()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube)
        

#随机生成一个初始乱的魔方
    def init(self,init_level=0):
        self.current_level = init_level
        self.init2(init_level)
        self.his_actions = []
        self.advice = ""
        self.my_playground.rebuild()
        self.my_playground.displayCube()   

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
            self.my_playground.cube().rotateCube(face,layer,clockwize)
        #rotate to F2L stage
        auto_actions = []
        init_stage = p_map[self.resolve_method][init_level]
        while self.stage < init_stage:
            for a in auto_actions:
                face = a_map[a]["face"]
                layer = a_map[a]["layer"]
                clockwize = a_map[a]["clockwize"]
                self.my_playground.cube().rotateCube(face,layer,clockwize)
            advice = self.hint2()
            auto_actions = parseAdvice(advice.get("h",""))
            if auto_actions == "":
                break
#进阶到下一个阶段
    def next(self,dummy):
        if self.current_level == -1:
            self.current_level = self.my_library.lib_level
        current_stage = p_map[self.resolve_method][self.current_level]
        self.current_level += 1
        if self.current_level >= len(p_map[self.resolve_method]):
            printLeft("魔方已经完全解决")
            return
        next_stage = p_map[self.resolve_method][self.current_level]
        auto_actions = []       
        while current_stage < next_stage:
            for a in auto_actions:
                face = a_map[a]["face"]
                layer = a_map[a]["layer"]
                clockwize = a_map[a]["clockwize"]
                self.my_playground.cube().rotateCube(face,layer,clockwize)
            advice = self.hint2()
            auto_actions = parseAdvice(advice.get("h",""))
            current_stage = advice.get("s",current_stage)
            if auto_actions == "":
                break
        self.his_actions = []
        self.advice = ""
        self.my_playground.rebuild()
        self.my_playground.displayCube() 
        self.current_level = -1		

    def help(self,dumy):
        if self.right_panel != "help":
            self.clearRight() 
            self.right_panel = "help"
            self.my_tutorial.nextOrPrevious(0)

    def snapshot(self,dumy): 
        if self.right_panel != "snapshot":
            self.right_panel = "snapshot"
            self.clearRight() 
    
        self.comparing = False
        self.my_snapshot.takeSnapshot(self.my_playground.cube())
   
    def compare(self,dumy):
        if self.comparing:#已经处于比对状态，先取消
            self.cancel(dumy)
        self.comparing = True        
        mark = 0
        right = None
        if self.right_panel == "snapshot":
            right = self.my_snapshot
        elif self.right_panel == "library":
            right = self.my_library
        else:
            self.comparing = False
            return
        for my_b in self.my_playground.blocks():        
            for sn_b in right.blocks():
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
                        
        if mark > 0:
            self.my_playground.displayCube()
            right.displayCube()

        
    def quit(self,dumy):
        self.gameExit = True

    def step(self,dumy):
        self.advice = self.hint2().get("h","")
        if self.advice != "End":
            self.my_playground.auto_actions = parseAdvice(self.advice)

    def delete(self,dumy):
        msg = ""
        if self.right_panel != "library":
            msg = u"当前是帮助窗口，不能删除."
        else:
            msg = self.my_library.deleteSnapshot()
        printLeft(msg)
        
    def hint(self,show):
        advice = self.hint2()
        t1 = advice.get("t1", None)
        t2 = advice.get("t2", None)
        for my_b in self.my_playground.blocks():
            if t1 != None:
                if (my_b.block.current.x == int(t1[0]) and
                    my_b.block.current.y == int(t1[1]) and my_b.block.current.z == int(t1[2])):
                        my_b.mark = "1"
            if t2 != None:
                if (my_b.block.current.x == int(t2[0]) and my_b.block.current.y == int(t2[1]) and
                   my_b.block.current.z == int(t2[2])):
                        my_b.mark = "2"
        if t1 != None:
            self.my_playground.displayCube()
        hint = advice.get("h","No Advise")
        printHint(hint)
        
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
        for my_b in self.my_playground.blocks():        
            if  my_b.mark != "-":
                my_b.mark = "-"
        if self.right_panel == "snapshot":
            right = self.my_snapshot
        elif self.right_panel == "library":
            right = self.my_library
                
        for sn_b in right.blocks():       
            if  sn_b.mark != "-":
                sn_b.mark = "-"
        self.my_playground.displayCube()
        right.displayCube()
           
    def cancel(self,dumy):
        if self.my_playground.brush_copy == 1:
            self.my_playground.cancelBrush() 
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.cancelComparing()
        else:#撤销上次的转动
            self.my_playground.singleRotate(None)    
        
    def library(self,level):
        if self.right_panel != "library":
            self.clearRight() 
            self.right_panel = "library"
            self.my_library.selectSnapshot()

    def method(self,method):
        self.resolve_method = method
        msg = "当前提示和自动解题方法是" + method
        printLeft(msg)
        
    def quitz(self,dummy):
        if self.right_panel != "library":
            self.right_panel = "library"
            self.clearRight()
        l = math.ceil(random.random() * 4)
        self.my_library.setLevel(l)
        self.current_level = l
        total = self.my_library.getTotal()
        r = int(random.random() * total)
        self.my_library.selectSnapshot(r)
        self.load(0)
        printLeft(u"当前是第" + str(r) + u"题")

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
                    if event.button == 1 and (not self.my_playground.rotating):
                        mouse_down_x,mouse_down_y = event.pos
                        mouse_status[0] = 0
                        mouse_status[1] = mouse_down_x
                        mouse_status[2] = mouse_down_y
                        hit_b,hit_f = self.my_playground.hitBlock(mouse_down_x,mouse_down_y)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and (not self.my_playground.rotating):
                        mouse_up_x,mouse_up_y = event.pos
                        mouse_status[0] = 1
                        mouse_status[1] = mouse_up_x
                        mouse_status[2] = mouse_up_y
                        if hit_f != -1:
                            action = self.my_playground.detectAction(hit_b,hit_f,
                                            (mouse_down_x,mouse_down_y),
                                            (mouse_up_x,mouse_up_y))
                            if action != "-":
                                self.my_playground.singleRotate(action)
                                self.dk_count = 0
                            else:    
                                self.dk_count += 1
                                if self.dk_count == 1:
                                    self.dk_time = pygame.time.get_ticks()
                                if self.dk_count == 2:
                                    self.dk_count = 0
                                    if (pygame.time.get_ticks() - self.dk_time) < 250:
                                        if self.my_playground.brush_copy == 1:
                                            self.my_playground.brushColor(hit_b,hit_f)
            
            b_h = y_scale*30
                
          #退出按钮，最右上角
            button(screen,"X",ft_sz,x_scale*1300,y_scale*10,x_scale*40,b_h,green,red,self.quit,"X")
          #显示控制按钮
            b_map = [[(u"题库",self.library,0),
                    ("7步",self.method,"Simple"),("F2CP",self.method,"F2CP"),
                    (u"保存",self.save,1),(u"帮助",self.help,0),
                    (u"删除",self.delete,0), (u"提示",self.hint,1),
                    (u"开始",self.reset,0)],
                     [(u"<-|",self.load,0),(u"|->",self.snapshot,0),
                     (u"对比",self.compare,0),("打乱",self.init,1),
                     (u"进阶",self.next,2),(u"出题",self.quitz,0),
                     (u"自动",self.step,0),(u"撤销",self.cancel,0),
                     ]]

            b_x = x_scale*790; b_y = y_scale*690; b_h = y_scale*30
            for bs in b_map:
                for b,f,p in bs:
                    if f != None:               
                        button(screen, b, ft_sz, b_x, b_y, x_scale*60,b_h,green,red,f,p)
                    else:
                        button(screen, b, ft_sz, b_x, b_y, x_scale*60,b_h,gray,red,f,p)
                    b_x += x_scale*70
                b_y += y_scale*40; b_x = x_scale*790
                     
            self.my_playground.displayButtons()                
            self.my_playground.displayRotation()
                  
            
            if self.right_panel == "library":
                self.my_library.displayHeader()
            elif self.right_panel == "help":
                self.my_tutorial.displayHeader()
           
            clock.tick(30)
            pygame.display.update()
    
  
