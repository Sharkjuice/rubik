# -*- coding: utf-8 -*-  
import pygame,time,os,random,subprocess,math
import cubeModel,cubeSnapshot,cubeTutorial,\
        cubeLibrary,cubePlayground
from cubeGlobal import mouse_status,m_map,a_map,\
        background,black,green,red,colors_r,colors_n,colors
from cubeCommon import button,printText
from macroParse import parseAdvice
from cubePanel import Panel


#0: init;1:bottom center ok;2:bottom edge ok;3 bottom corner ok
#4:layer 2 OK;#5:up color OK;#6:Game Over
p_map = {
"Simple":[0,1,2,3,4,5,6],
"F2CP":[0,1,2,4,5,6]
}


class CubeControl:
    def __init__(self, init_count, his_count,init_level=2):
        self.init_count = init_count
        self.resolve_method = "F2CP"
        self.right_panel = "library"

        self.gameExit = False
        self.current_level = init_level
        self.dk_count = 0
        self.dk_time = 0

        self.comparing = False
        #初始化数据模型,判断mycube.clp文件在不在，
        #如果在，就读这个文件初始化
        if os.path.exists("./mycube.clp"):
            my_cube = cubeModel.Cube("./mycube.clp")
        else:
            my_cube = cubeModel.Cube()
        self.my_playground = cubePlayground.CubePlayground(my_cube)
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube)
        self.my_tutorial = cubeTutorial.CubeTutorial()       
        self.my_library = cubeLibrary.CubeLibrary(my_cube,init_level)
       
    def displayAll(self):
        self.my_playground.displayContent()
        #self.my_tutorial.displayContent() 
        self.my_library.displayContent()		
        Panel.printLeft(u"当前解题方法是" + self.resolve_method + u"法")
        Panel.printHint(u"下一步提示")

    #flag:0 保存为mycube.clp为了进行规则计算;1:保存为mycubexx.clp
    def save(self,dumy):
        if self.right_panel != "library":
            Panel.clearRight() 
            self.right_panel = "library"
    
        self.my_library.saveCube(self.my_playground.cube())
                                         
    #非界面调用    
    def save2(self,figure):
        self.my_library.saveCube2(self.my_playground.cube(),
                                 figure)            
            
    def load(self,dumy):
        cube = None
        if self.right_panel == "snapshot":
            cube = self.my_snapshot.cube()
        elif self.right_panel == "library":
            cube = self.my_library.cube()
        if cube != None:
            self.my_playground.load(cube)
            self.my_playground.rebuild()            
            self.my_playground.displayContent()
 
    def reset(self,dumy):
        my_cube = cubeModel.Cube()
        self.my_playground = cubePlayground.CubePlayground(my_cube) 
        self.my_playground.displayContent()
        self.my_snapshot = cubeSnapshot.CubeSnapshot(my_cube)
        

#随机生成一个初始乱的魔方
    def init(self,init_level=0):
        self.current_level = init_level
        self.init2(init_level)
        self.his_actions = []
        self.advice = ""
        self.my_playground.rebuild()
        self.my_playground.displayContent()   

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
            Panel.printLeft("魔方已经完全解决")
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
        self.my_playground.displayContent() 
        self.current_level = -1     

    def help(self,dumy):
        if self.right_panel != "help":
            Panel.clearRight() 
            self.right_panel = "help"
            self.my_tutorial.nextOrPrevious(0)

    def snapshot(self,dumy): 
        if self.right_panel != "snapshot":
            self.right_panel = "snapshot"
            Panel.clearRight() 
    
        self.comparing = False
        self.my_snapshot.takeSnapshot(self.my_playground.cube())
   
    def compare(self,dumy):
        if self.right_panel != "snapshot":
            Panel.printLeft("没有快照可以比较!")
            return
        if self.comparing:#已经处于比对状态，先取消
            self.cancel(dumy)
        self.comparing = True        
        mark = 0
        right = self.my_snapshot
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
            self.my_playground.displayContent()
            self.my_snapshot.displayContent()

        
    def quit(self,dumy):
        self.gameExit = True

    def step(self,dumy):
        self.advice = self.hint2().get("h","")
        if self.advice != "End":
            self.my_playground.auto_actions = parseAdvice(self.advice)

    def delete(self,dumy):
        if self.right_panel != "library":
            Panel.printLeft(u"当前是帮助窗口，不能删除.")
        else:
            self.my_library.deleteCurrent()
        
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
            self.my_playground.displayContent()
        hint = advice.get("h","No Advise")
        Panel.printHint(hint)
        
    def hint2(self):
        self.save2(0)
        if self.resolve_method == "F2CP":
            res = subprocess.Popen("clipsutil.exe rubik-flcp.clp",bufsize = 1,shell = True,stdout=subprocess.PIPE)
        else:
            res = subprocess.Popen("clipsutil.exe rubik-simple.clp",bufsize = 1,shell = True,stdout=subprocess.PIPE)
        outlines = res.stdout.readlines()
        adv_p = []
        for outline in outlines:
            ##print(outline)
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
        ##print(best[0])
        return best[0]

    def cancelComparing(self):
        if self.right_panel != "snapshot":
            Panel.printLeft("没有快照可以取消比较!")
            return
	
        self.comparing = False        
        mark = 1
        for my_b in self.my_playground.blocks():        
            if  my_b.mark != "-":
                my_b.mark = "-"
        for sn_b in self.my_snapshot.blocks():       
            if  sn_b.mark != "-":
                sn_b.mark = "-"
        self.my_playground.displayContent()
        self.my_snapshot.displayContent()
           
    def cancel(self,dumy):
        if self.my_playground.brush_copy == 1:
            self.my_playground.cancelBrush() 
        elif self.comparing:#已经处于比对状态，先撤销次状态
            self.cancelComparing()
        else:#撤销上次的转动
            self.my_playground.singleRotate(None)    
        
    def library(self,level):
        if self.right_panel != "library":
            Panel.clearRight() 
            self.right_panel = "library"
            self.my_library.displayContent()

    def method(self,method):
        self.resolve_method = method
        Panel.printLeft("当前提示和自动解题方法是" + method)
        
    def quitz(self,dummy):
        if self.right_panel != "library":
            self.right_panel = "library"
            Panel.clearRight()
        l = math.ceil(random.random() * 4)
        self.my_library.setLevel(l)
        self.current_level = l
        total = self.my_library.getTotal()
        r = math.ceil(random.random() * total)
        self.my_library.setCurrent((-1,r))
        self.my_library.displayContent()
        self.load(0)
        Panel.printLeft(u"当前是第" + str(r) + u"题")

    #mouse single click
    def singleClick(self,x,y):
        #print("single click...",x,y)
        if self.my_playground.singleClick(x,y):
            #print("playground sinlge clicked")
            return True
        if self.right_panel == "library":
            if self.my_library.singleClick(x,y):
                #print("library single clicked")
                return True
        #print("No single click action!")
        return False
    
    #判断是否是双击鼠标
    def isContEvent(self,txy1,txy2):
        #print("is double click?",txy1,txy2)
        t_gap = txy2[0] - txy1[0]
        x_gap = txy2[1] - txy1[1]
        y_gap = txy2[2] - txy1[2]
        r_gap = x_gap*x_gap + y_gap*y_gap
        if t_gap < 250 and r_gap < 25:
            #print("Yes, is double click")
            return True
        #print("No, is not double click")
        return False

    #mouse double click
    def doubleClick(self):
        #print("doubleClick")
        if self.my_playground.doubleClick():
            #print("playground double clicked")
            return True
        if self.my_library.doubleClick():
            #print("library double clicked ")
            cube = self.my_library.cube()
            self.my_playground.load(cube)
            self.my_playground.rebuild()            
            self.my_playground.displayContent()
            return True
        #print("No double click action!")
        return False
    
    #mouse drag
    def drag(self,xy1,xy2):
        if self.my_playground.drag(xy1,xy2):
            #print("playground draged")
            return True
        #print("No drag action")
        return False
    
    def gameLoop(self):
        global mouse_status
        pre_mouse_txy = (0,0,0)
        click_times = 0
        clock = pygame.time.Clock()
        screen,ft_sz,x_scale,y_scale= Panel.screen, \
             Panel.ft_sz,Panel.x_scale,Panel.y_scale
        while not self.gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                    
                    self.gameExit = True
                if event.type == pygame.KEYDOWN:                    
                    if event.key == pygame.K_ESCAPE:
                        self.gameExit = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and (not self.my_playground.rotating):
                        mouse_x,mouse_y = event.pos
                        mouse_t = pygame.time.get_ticks()
                        mouse_status[0] = 1
                        mouse_status[1] = mouse_x
                        mouse_status[2] = mouse_y
                        #print("Mouse button down detected")
                        if self.isContEvent(pre_mouse_txy,
                                              (mouse_t,mouse_x,
                                               mouse_y),
                                              ):
                            self.doubleClick()
                        else:
                            self.singleClick(mouse_x,mouse_y)
                        pre_mouse_txy = (mouse_t,mouse_x,mouse_y)						
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and (not self.my_playground.rotating):
                        mouse_x,mouse_y = event.pos
                        mouse_t = pygame.time.get_ticks()
                        #print("Mouse button up detected")
                        if not self.isContEvent((mouse_t,mouse_x,
                                               mouse_y),
                                              pre_mouse_txy):
                            self.drag((pre_mouse_txy[1], pre_mouse_txy[2]),
                                     (mouse_x,mouse_y))
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
                     
            self.my_playground.displayHeader()                
            self.my_playground.displayRotation()
                  
            
            if self.right_panel == "library":
                self.my_library.displayHeader()
            elif self.right_panel == "help":
                self.my_tutorial.displayHeader()
           
            clock.tick(50)
            pygame.display.update()
    
  
