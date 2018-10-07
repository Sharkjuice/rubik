import argparse,pygame,sys
from cubeControl import  CubeControl
from cubePanel import Panel 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", type = int,help="automatically resolve to this level")   
    parser.add_argument("--gen", type = int,help="just to genaerate F2CP samples.")    
    args = parser.parse_args()
    if args.auto == None:
        args.auto = 2  
    Panel.display()
	#19:打乱魔方随机转19步;25:历史记录
    cubeControl = CubeControl(19,25,args.auto)  
    cubeControl.displayAll()	
    cubeControl.gameLoop()
    pygame.quit()
    sys.exit()
  
