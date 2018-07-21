import argparse,pygame,ctypes
from cubeControl import  CubeController
from cubeGlobal import setDisplayParams,background 

#屏幕的最小宽度和高度
min_scn_w = 1350
min_scn_h = 768
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", help="automatically resolve to this level")	
    args = parser.parse_args()
    if args.auto == None:
        args.auto = 2    
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

    cubeController = CubeController(15,25,int(args.auto))
    
    cubeController.gameLoop()
    pygame.quit()
  