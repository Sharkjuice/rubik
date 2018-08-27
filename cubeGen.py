import argparse,pygame,ctypes
from cubeControl import  CubeControl
from cubeGlobal import setDisplayParams,background 
from cubePanel import CubePanel 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", type = int,help="automatically resolve to this level")   
    parser.add_argument("--gen", type = int,help="just to genaerate F2CP samples.")    
    args = parser.parse_args()
    if args.auto == None:
        args.auto = 2  
    cubeControl = CubeControl(19,25,args.auto)
    if args.gen == 1:
        fig_num = {1:14,2:41,3:57,4:21}
        figures = []
        generated = 0;i=0
        print("I will try ", fig_num[args.auto]*5, " times. Pls wait.")
        while i < fig_num[args.auto]*5 and generated < fig_num[args.auto]:
            cubeController.init2(args.auto)
            fig = cubeController.hint2().get("f",0)
            i += 1
            print(u"Try ", i, " times...")
            if fig !=0:
                if cubeController.figure not in figures:
                    cubeController.save2(1,fig)
                    figures.append(fig)
                    generated += 1
                    print(u"Success ", generated, " times!")
    
    cubeControl.gameLoop()
    pygame.quit()
  
