import argparse,pygame,ctypes
from cubeControl import  CubeController
from cubeGlobal import setDisplayParams,background 

#屏幕的最小宽度和高度
min_scn_w = 1350
min_scn_h = 768
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", type = int,help="automatically resolve to this level")   
    parser.add_argument("--gen", type = int,help="just to genaerate F2CP samples.")    
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
    
    #最外面的框
    pygame.draw.rect(screen,(128,128,128),(0,0,scn_w-1,scn_h-1),2)
    #pygame.draw.line(screen,(128,128,128),pt2,pt4,2)
    #pygame.draw.line(screen,(128,128,128),pt4,pt3,2)
    #pygame.draw.line(screen,(128,128,128),pt3,pt1,2)
    #竖分割线
    pygame.draw.line(screen,(128,128,128),(x_scale*800,0),(x_scale*800,y_scale*680),2)
    #底部横线
    pygame.draw.line(screen,(128,128,128),(x_scale*210,y_scale*680),(scn_w-2,y_scale*680),2)
    #底部竖线
    pygame.draw.line(screen,(128,128,128),(x_scale*210,y_scale*680),(x_scale*210,scn_h*680),2)
	
    cubeController = CubeController(19,25,args.auto)
    cubeController.level(args.auto)
    if args.gen == 1:
        fig_num = {1:14,2:41,3:57,4:21}
        figures = []
        generated = 0;i=0
        print("I will try ", fig_num[args.auto]*5, " times. Pls wait.")
        while i < fig_num[args.auto]*5 and generated < fig_num[args.auto]:
            cubeController.init(0)
            fig = cubeController.hint2().get("f",0)
            i += 1
            print(u"Try ", i, " times...")
            if fig !=0:
                if cubeController.figure not in figures:
                    cubeController.save2(1,fig)
                    figures.append(fig)
                    generated += 1
                    print(u"Success ", generated, " times!")
    
    cubeController.gameLoop()
    pygame.quit()
  
