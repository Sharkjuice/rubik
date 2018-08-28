# -*- coding: utf-8 -*-
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

colors = {"r":(255,0,0),"g":(0,255,0),"o":(255,0,255),"w":(255,255,255),
      "b":(0,0,255),"y":(255,255,0),"-":(128, 128, 128)}

colors_r = {(255,0,0):"r",(0,255,0):"g",(0,0,255):"b",(255,255,255):"w",
      (255,0,255):"o",(255,255,0):"y",(128, 128, 128):"-"}

colors_n = {"r":u"红色","g":u"绿色","b":u"紫色","w":u"白色",
      "o":u"蓝色","y":u"黄色","-":u"灰色"}
	  
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

m_map = [["FRUR'","F'UF","FU'F'","RUR'","RU'R'","R'U'R",
			"R'UR"],
		 ["RU2R'","RUR'U","R'U'RU'","R'U2R","R'FRF'","RUR'U'",
			"RU'R'U"],	
	     ["RU'R'U'","R'U'RU'","U'R'UR","U'RU'R'","rUR'U'","r'U'RU'",
			"rU2R'",
			],			
	     ["r'U2R","UR'Ur","rUr'","rU'r'","r'U'r","r'Ur","r'FRF'"],
	     ["(UR'U'R)2","(URU'R')2","(R'U'RU)2","(RUR'U')2",
			"(U'RUR')2","RUR'F'","RU'R'D"],					
	     ["FRUR'U'F'","fRUR'U'f'","B'U'R'URB","FURU'R'F'",
			"R2U'R'U'","R2UR'U'","R2u'RU'"],
	     ["UR'uR2","R2uR'U","U'Ru'R2","FRU'R'",
			"RUR'F'","M2U","RU"]
			
		]

#背景颜色
background = (32,32,32)

#字体前景颜色
black = (0,0,0)
#在蓝色背景上的字体颜色
white = (255,255,255)
#按钮颜色
green = (0,255,0)
#按钮按下后的颜色
red = (240,0,0)

mouse_status=[0,0,0]

    
