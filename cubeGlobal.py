# -*- coding: cp936 -*-
import operator, copy
#x轴：水平向右；y轴：垂直向上；z轴：向屏幕里面，圆心在魔方中心块
cube_i = [
	((-1, -1, -1), "rwg"), ((-1, 0, -1), "r-g"), ((-1, 1, -1), "ryg"), 
	((-1, -1,0), "rw-"), ((-1, 0, 0), "r--"), ((-1, 1, 0), "ry-"), 
	((-1, -1, 1), "rwo"), ((-1, 0, 1), "r-o"), ((-1, 1, 1), "ryo"),
	
	((0, -1, -1), "-wg"), ((0, 0, -1), "--g"), ((0, 1, -1), "-yg"), 
	((0, -1, 0), "-w-"), ((0, 0, 0), "---"), ((0, 1, 0), "-y-"), 
	((0, -1, 1), "-wo"), ((0, 0, 1), "--o"), ((0, 1, 1), "-yo"),

	((1, -1, -1), "bwg"), ((1, 0, -1), "b-g"), ((1, 1, -1), "byg"), 
	((1, -1, 0), "bw-"), ((1, 0, 0), "b--"), ((1, 1, 0), "by-"), 
	((1, -1, 1), "bwo"), ((1, 0, 1), "b-o"), ((1, 1, 1), "byo")
]

cube_o = {
        #F面右下角，自下向上
	(-1, -1, -1):[(0,3),{0:{"U":"F'", "Ru":"D","DC":"F"}, 3:{"U":"R", "Lu":"D'","DC":"D"}}],
        (-1, 0, -1):[(0,3),{0:{"Ru":"u'","U":"f'","DC":"u"},3:{"Lu":"u","U":"r","DC":"u'"}}],                      
        (-1, 1, -1):[(0,3,4),{0:{"D":"F", "Ru":"U'","DC":"U"},
                                3:{"D":"R'","Lu":"U","DC":"R"},
                                4:{"Lu":"F'","Ru":"R","DC":"F"}}],
        #F面中排，自下向上
	(-1, -1,0):[(3),{3:{"U":"r","DC":"r'"}}],
        (-1, 0, 0):[(3),{3:{"U":"x","D":"x'","Lu":"y","Rd":"y'","DC":"x"}}],        
        (-1, 1, 0):[(3,4),{3:{"D":"r'","DC":"r"}, 4:{"Ru":"r","DC":"r'"}}],
        #F面左排，自下向上
	(-1, -1, 1):[(3),{3:{"U":"L'","Rd":"D","DC":"L"}}],       
        (-1, 0, 1):[(3),{3:{"Rd":"u'","DC":"u"}}],        
        (-1, 1, 1):[(3,4),{3:{"D":"L", "Rd":"U'","DC":"U"},
                            4:{"Ru":"L'","Rd":"F","DC":"L"}}],
        #R面中排，自下向上
	(0, -1, -1):[(0),{0:{"U":"f'","DC":"f"}}],        
        (0, 0, -1):[(0),{0:{"U":"z'","D":"z","Ld":"y","Ru":"y'","DC":"z'"}}],        
        (0, 1, -1):[ (0,4),{0:{"D":"f","DC":"f'"}, 4:{"Lu":"f'","DC":"f"}}],
        #R面右排
	(1, -1, -1):[(0),{0:{"U":"B", "Ld":"D'","DC":"D"}}],
        (1, 0, -1): [(0),{0:{"Ld":"u","DC":"u'"}}],
        (1, 1, -1):[ (0,4),{0:{"D":"B'","Ld":"U","DC":"B"}, 4:{"Ld":"R'","Lu":"B","DC":"R"}}],
        #U面
	(1, 1, 0):[(4),{4:{"Ld":"r'","DC":"r"}}],
        (1, 1, 1):[(4),{4:{"Ld":"L","Rd":"B'","DC":"B"}}],
	(0, 1, 0):[(4),{4:{"Lu":"z'","Rd":"z","Ld":"x'","Ru":"x","DC":"z"}}],        
        (0, 1, 1):[(4),{4:{"Rd":"f","DC":"f'"}}],
        
         }

cube_f = [[(-1,y,z)  for y in [-1,0,1] for z in [-1,0,1]],
          [( 0,y,z)  for y in [-1,0,1] for z in [-1,0,1]],
          [( 1,y,z)  for y in [-1,0,1] for z in [-1,0,1]]
          ]

cube_u = [[(x, 1,z)  for x in [-1,0,1] for z in [-1,0,1]],
          [(x, 0,z)  for x in [-1,0,1] for z in [-1,0,1]],
          [(x,-1,z)  for x in [-1,0,1] for z in [-1,0,1]]
          ]
cube_r = [[(x,y,-1)  for x in [-1,0,1] for y in [-1,0,1]],
          [(x,y, 0)  for x in [-1,0,1] for y in [-1,0,1]],
          [(x,y, 1)  for x in [-1,0,1] for y in [-1,0,1]]
	  ]
faces = {"FRONT":cube_f,"UP":cube_u,"RIGHT":cube_r}

colors = {"r":(255,0,0),"g":(0,255,0),"b":(0,0,255),"w":(255,255,255),
	  "o":(255,0,255),"y":(255,255,0),"-":(128, 128, 128)}
background = (32,32,32)

#0,1,2,3为正面的4个点， 4,5,6,7位背面的4个点
block_v = [(x,y,z) for z in (-0.5,0.5) for y in (0.5,-0.5) for x in (-0.5,0.5)]
screen = None		  
win_height = 768
win_width = 800
fov = 700
distance = 8

#按钮颜色
red = (255,0,0)
black = (0,0,0)
green = (0,255,0)
bright_green = (240,0,0)
bright_red = (0,240,0)

