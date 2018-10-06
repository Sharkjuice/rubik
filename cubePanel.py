import pygame,ctypes
from cubeGlobal import background,black
from cubeCommon import printText

#屏幕的最小宽度和高度
min_scn_w = 1350
min_scn_h = 768
 
class Panel():
    #文本框背景颜色
    gray = (128,128,128)

    @classmethod
    def display(cls):
        #初始化pygame屏幕
        pygame.init()
        ctypes.windll.user32.SetProcessDPIAware()
        scn_w, scn_h = (ctypes.windll.user32.GetSystemMetrics(0),
                       ctypes.windll.user32.GetSystemMetrics(1))
        cls.screen = pygame.display.set_mode((scn_w, scn_h),
                                         pygame.FULLSCREEN)
        cls.screen.fill(background)
        pygame.display.set_caption("3D魔方教程")
        cls.x_scale = scn_w/min_scn_w
        cls.y_scale = scn_h/min_scn_h
        cls.ft_sz = int(cls.x_scale*25)
        
        #setDisplayParams(screen,25,x_scale,y_scale)    
        pt1 = (0,0)# top left point
        pt2 = (scn_w-2,0)#top right point
        pt3 = (0, scn_h-2)#bottom left point
        pt4 = (scn_w-2, scn_h-2)
        
        #最外面的框
        pygame.draw.rect(cls.screen,(128,128,128),
                            (0,0,scn_w-1,scn_h-1),
                                               2)
        #竖分割线
        pygame.draw.line(cls.screen,(128,128,128),
                              (cls.x_scale*810,0),
                (cls.x_scale*810,cls.y_scale*680),
                                               2)
        #底部横线
        pygame.draw.line(cls.screen,(128,128,128),
                (cls.x_scale*210,cls.y_scale*680),
                        (scn_w-2,cls.y_scale*680),
                                               2)
        #底部竖线
        pygame.draw.line(cls.screen,(128,128,128),
                (cls.x_scale*210,cls.y_scale*680),
                      (cls.x_scale*210,scn_h*680),
                                               2)
    
    @classmethod
    def printLeft(cls,msg): 
        #screen,ft_sz,x_scale,y_scale= getDisplayParams()
        pygame.draw.rect(
            cls.screen,cls.gray,
            (cls.x_scale*220,cls.y_scale*690,
             cls.x_scale*560,cls.y_scale*30))            
        printText(
            cls.screen, msg, "fangsong", 
            cls.ft_sz, cls.x_scale*225, 
            cls.y_scale*693, background)

    @classmethod
    def printHint(cls,msg): 
        #screen,ft_sz,x_scale,y_scale= getDisplayParams()
        if msg != "":
            pygame.draw.rect(cls.screen,cls.gray,(cls.x_scale*220,
                   cls.y_scale*730,cls.x_scale*560,cls.y_scale*30))            
            printText(cls.screen, msg, "fangsong", cls.ft_sz, 
                cls.x_scale*225, cls.y_scale*733, background)

    @classmethod
    def printRight(cls,msg):    
        #screen,ft_sz,x_scale,y_scale= getDisplayParams()
        if msg != "":
            pygame.draw.rect(
                cls.screen,cls.gray,
                (cls.x_scale*1170, cls.y_scale*640,
                 cls.x_scale*170, cls.y_scale*30))            
            printText(cls.screen, msg, "fangsong", cls.ft_sz, 
                    cls.x_scale*1175, cls.y_scale*643, black)

    @classmethod
    def clearRight(cls):
        right_x = cls.x_scale*815
        right_y = cls.y_scale*5
        right_w = cls.x_scale*535
        right_h = cls.y_scale*675
        pygame.draw.rect(cls.screen,background,
              (right_x,right_y,right_w,right_h))
        
