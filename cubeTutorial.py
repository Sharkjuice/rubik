# -*- coding: utf-8 -*-  
import pygame
from cubeGlobal import background,green,red,\
	white,colors,getDisplayParams
from cubeCommon import button,printText
steps = [
{"step":u"前提", "title":u"基本常识",
"text":[
u"1. 魔方有6面，6种颜色。总共有27个块，",
u"其中有8个角块，12个棱块，6个中心块。",
u"每个角块有3个面，棱块有2个面， 中心",
u"块有一个面。转动时中心面位置不变。",
u"2. 我们把魔方拿在手上，左前方左后方别",
u"为F/B面(图8-1),右前方右后方分别为R/L",
u"面(图8-2)；最上最下层分别为U/D面(图8",
u"-3),小写字母表示大写字母加中间层。",
u"3. 左边按钮，分别表示转动该面，加撇",
u"的表示逆时针转，不加撇表示顺时针转。",
u"每次操作都是旋转90度。"],
"figures":[(7,0),(7,1),(7,2)]
     },
{"step":u"第一步", "title":u"底层十字还原",
"text":[
u"找到白色中心块，定为底面, 然后把4个带",
u"有白色面的棱块移至顶面，观察白色棱块侧",
u"面颜色,转动底下两层与对应中心块对齐(如",
u"图1-1)将4个白色棱移至底面。这样完成一",
u"个底层十字，并且十字侧面颜色和中心块对",
u"齐(如图1-3)。当白色块在顶层需要翻转时(",
u"如图1-2)，使用公式1。",
u"",
u"公式1: F R U"],
"figures":[(0,0),(0,1),(0,2)]
},    
{"step":u"第二步", "title":u"底角归位(1)",
"text":[
u"复原魔方第一层四个角会出现两种情况:  ",
u"1. 在顶层面找到一个有白色面的角块,转",
u"动顶层，将角块放置前层右上角位置,观察",
u"角块另外两个颜色,转动魔方底下两层直到",
u"到与前面和右面中心块颜色相对应(如图2-1",
u",2-2, 2-3)。图2-1使用公式2-1。图2-2使",
u"用公式2-2。图2-3使用公式2-3，变成情况",
u"1，再使用公式2-1。",
u"",
u"公式2-1：R U R' "
u"公式2-2: F' U' F",
u"公式2-3：RUU R'U'" ],
"figures":[(1,0),(1,1),(1,2)]
},
{"step":u"第二步", "title":u"底角归位(2)",
"text":[
u"2. 如果底层没有复原，顶层也没有带白色",
u"面的角块，观察底层找到位置错误的角块，",
u"放至前层右下角位置（如图2-4，2-5), 图",
u"2-4使用公式2-4变成图2-1；图2-5使用公",
u"式2-5,变成图2-2。 再分别使用前述方法", 
u"就可完成。",
u"",
u"公式2-4：RUR'U'", 
u"公式2-5：F' U' F U"],
"figures":[(1,3),(1,4)]
},
{"step":u"第三步", "title":u"中层棱块归位(1)",
"text":[
u"首先需要在顶层找到一个没有黄色面的棱块，",
u"转动上层，将棱块侧面颜色和中心颜色对齐",
u"，我们把对齐后的这面定义为右面，观察棱",
u"块上面的颜色，此时会出现两种情况：",
u"1. 与前面中心块颜色一致(如图3-1)，此时",
u"需要用公式3-1，棱块就能复位至前面位置。",
u"2. 如果与前面中心块颜色不一致(如图3-2)，",
u"需要用公式3-2，就能复原到后层棱块位置。",
u"",
u"公式3-1：R'U'R'U'R' URUR(五逆四顺) ",
u"公式3-2：RURUR U'R'U'R'(五顺四逆)"],
"figures":[(2,0),(2,1)]
},

{"step":u"第三步", "title":u"中层棱块归位(2)",
"text":[
u"3. 特殊情况：当中层出现棱块需要调整方",
u"向时需要将棱块放于前层右棱块位置(如图",
u"3-3),转动公式3-1就能将棱块移至顶层，再",
u"按照情况1或情况2的方法即可完成。",
u"",
u"公式3-1：R'U'R'U'R' URUR(五逆四顺) ",
u"公式3-2：RURUR U 'R'U'R'(五顺四逆)"],
"figures":[(2,2)]
},

{"step":u"第四步", "title":u"顶面架十字",
"text":[
u"第三层的还原需要在顶面架一个黄色'十字'",
u"架。在架十字的时候回出现三种情况。",
u"1.顶面已经有黄色块连成'一'字(如图4-1) ",
u"这时需要转动公式4，就能加架好顶面黄色",
u"十字架。",
u"2.顶面已经有黄色棱块连成直角，把它定位",
u"左上直角(如图4-2)，转动公式4，就变成情",
u"况1，按照情况1的方法就能将顶层十字架好。",
u"3.顶层只有一个黄色中心块(如图4-3)，这时",
u"我们需要任意方向转动一次公式4就转变成情",
u"况2，再用情况2的方法就能将顶层十字架好。",
u"",
u"公式4： F R U R' U' F'"],
"figures":[(3,0),(3,1),(3,2)]
},
{"step":u"第五步", "title":u"顶角面归位(1)",
"text":[
u"这一步我们需要将顶层黄色面归位，会出现",
u"三种情况：",
u"1. 顶面只有一个黄色角块，转动顶面至右",
u"前角位置(图5-1)，转动公式5即可完成。若",
u"没有复原，对好角块位置后，再重复一次公",
u"式5-1，即可完成。",
u"",
u"公式5-1：R' U2 RU R' UR"],
"figures":[(4,0)]
},    
{"step":u"第五步", "title":u"顶角面归位(2)",
"text":[
u"2. 顶面有两个黄色的角块，转动顶层直到",
u"右面的左上角出现黄色角块面(如图5-2、5-",
u"3、5-4),再转动公式5后变成情况1。按情况",
u"1的方法即可完成。",
u"",
u"公式5-1：R' U2 RU R' UR"],
"figures":[(4,1),(4,2),(4,3)]
},
{"step":u"第五步", "title":u"顶角面归位(3)",
"text":[
u"3. 顶面没有黄色的角块，转动顶层直到前",
u"面右上角位置出现黄色角块面(如图5-5)，",
u"转动公式5-1后变成情况1。",
u"",
u"公式5-1：R' UU RU R' UR",
u"公式5-1本质是对角互换， 其中一角不变(",
u"右面左上角），其它角原地顺时针旋转120",
u"后再换位。 因此观察，如果需要逆时针旋", 
u"可以用下面公式：",
u"",
u"公式5-2：F UU F' U' F U' F'"],
"figures":[(4,4)]
},
    
{"step":u"第六步", "title":u"顶角归位",
"text":[
u"顶层所有角块调整到正确位置的时候回出现",
u"两种情况：",
u"1. 在顶层侧面找到有两个相同颜色的角块，",
u"把这一面定位为前面(如图6-1)，转动公式6",
u"即可完成。",
u"2. 若顶层侧面没有找到两个相同颜色的角",
u"块(如图6-2)，转动公式6就会变成情况1。",
u"",
u"公式6：l U' R D2 R' UR D2 R2",    
u"公式6本质上是三角逆时针互换（顶面右上角",
u"不参与移动）"],
"figures":[(5,0),(5,1)]
},    
{"step":u"第七步", "title":u"顶棱归位",
"text":[
u"在顶棱归位时会出现两种情况：",
u"1. 顶层四个棱块中，有一个已经处于正确",
u"位置, 我们把这一面定为B面(如图7-1)，",
u"转动公式7-1 一次或两次即可完成。",
u"2. 若顶层没有棱块在正确的位置(如图7-2)",
u"转动公式7就会变成情况1。",
u"",
u"公式7：(RU'R)(URUR)(U'R'U'R')R'",          
u"公式7-1本质上是三个棱逆时针互换。因此",
u"需要使用两次公式。这时如果使用公式7-2",
u"可以实现逆时针互换，就只需要使用一次。",
u"",
u"公式7-2：R(RURU)(R'U'R'U')(R'UR')"],
"figures":[(6,0),(6,1)]
}    
]

figList = [
   
#第1步
[("---gbwwww","---rr----","-wwwyw-ww"),
("---wb----","---rr----","-b-wyw-w-"),
("---rr----","---bb----","-w-www-w-")],
#第2步
[("b---bb--b","w---rr--r","r--------"),
("w---bb--b","r---rr--r","b--------"),
("r---bb--b","b---rr--r","w--------"),
("--r-bb--b","--w-rr--r","---------"),
("--w-bb--b","--b-rr--r","---------")],
#第3步
[("--b-bb-bb","--rrrr-rr","---by----"),
("--b-bb-bb","--rrrr--r","---gy----"),
("-rb-bb-bb","-br-rr-rr","----y----")],
#第4步
[
("-bbybb-bb","-rr-rr-rr","---yyy---"),
("-bbybb-bb","-rryrr-rr","----yy-y-"),
("-bbybb-bb","-rryrr-rr","----y----")],
#第5步
[("-bb-bb-bb","-rr-rr-rr","yy-yyy-y-"),
("-bb-bb-bb","yrr-rr-rr","-yyyyyyy-"),
("-bb-bb-bb","yrr-rr-rr","-y-yyyyyy"),
("-bb-bb-bb","yrr-rryrr","-yyyyy-yy"),
("ybb-bb-bb","-rr-rr-rr","-y-yyy-y-")],
#第6步
[("gbb-bbgbb","-rr-rr-rr","yyyyyyyyy"),
("bbb-bbgbb","rrr-rrorr","yyyyyyyyy")],
#第7步
[("bbb-bbbbb","rrrgrrrrr","yyyyyyyyy"),
("bbb-bbbbb","rrrgrrrrr","yyyyyyyyy")],
#第0步
[("---------","yyyrrrggg","yyyrrrggg"),
("yyyrrrggg","---------","yrgyrgyrg"),
("yrgyrgyrg","yrgyrgyrg","---------")],
] 

f_points = [
(0,0),(0,20),(0,40),(0,60),(-16,-12),(-16,8),(-16,28),(-16,48),
(-32,-24),(-32,-4),(-32,16),(-32,36),(-48,-36),(-48,-16),(-48,4),(-48,24)
]
faces = [(0,1,5,4),(1,2,6,5),(2,3,7,6),(4,5,9,8),(5,6,10,9),
           (6,7,11,10),(8,9,13,12),(9,10,14,13),(10,11,15,14)]

r_points = [
(0,0),(0,20),(0,40),(0,60),(16,-12),(16,8),(16,28),(16,48),
(32,-24),(32,-4),(32,16),(32,36),(48,-36),(48,-16),(48,4),(48,24)
]

u_points = [
(0,0),(-16,-12),(-32,-24),(-48,-36),(16,-12),(0,-24),(-16,-36),(-32,-48),
(32,-24),(16,-36),(0,-48),(-16,-60),(48,-36),(32,-48),(16,-60),(0,-72)
]

class CubeTutorial:
    def __init__(self):
        self.currentStep = 0
        self.refresh = 1
        
    def nextOrPrevious(self,isNext):
        self.currentStep += isNext
        self.refresh = 1
        if self.currentStep < 0:
            self.currentStep = 0
        elif self.currentStep > 11:
            self.currentStep = 11
        self.displayTutorial()
    

    def displayFigure(self,screen,x,y,figure):
        f_colors = [colors[c] for c in figure[0]]
        r_colors = [colors[c] for c in figure[1]]
        u_colors = [colors[c] for c in figure[2]]
        i = 0
        for f in faces:
            pointlist = [(r_points[f[0]][0]+x, r_points[f[0]][1]+y),(r_points[f[1]][0]+x, r_points[f[1]][1]+y),
                         (r_points[f[2]][0]+x, r_points[f[2]][1]+y),(r_points[f[3]][0]+x, r_points[f[3]][1]+y)]
            pygame.draw.polygon(screen,r_colors[i],pointlist)   
            pointlist = [(r_points[f[0]][0]+x, r_points[f[0]][1]+y),(r_points[f[1]][0]+x, r_points[f[1]][1]+y),
                         (r_points[f[2]][0]+x, r_points[f[2]][1]+y),(r_points[f[3]][0]+x, r_points[f[3]][1]+y)]        
            pygame.draw.polygon(screen,(0,0,0),pointlist,1)
            i += 1
        i = 0        
        for f in faces:
            pointlist = [(f_points[f[0]][0]+x, f_points[f[0]][1]+y),(f_points[f[1]][0]+x, f_points[f[1]][1]+y),
                         (f_points[f[2]][0]+x, f_points[f[2]][1]+y),(f_points[f[3]][0]+x, f_points[f[3]][1]+y)]
            pygame.draw.polygon(screen,f_colors[i],pointlist)
            pointlist = [(f_points[f[0]][0]+x, f_points[f[0]][1]+y),(f_points[f[1]][0]+x, f_points[f[1]][1]+y),
                         (f_points[f[2]][0]+x, f_points[f[2]][1]+y),(f_points[f[3]][0]+x, f_points[f[3]][1]+y)]        
            pygame.draw.polygon(screen,(0,0,0),pointlist,1)
            i += 1
        i = 0
        for f in faces:
            pointlist = [(u_points[f[0]][0]+x, u_points[f[0]][1]+y),(u_points[f[1]][0]+x, u_points[f[1]][1]+y),
                          (u_points[f[2]][0]+x, u_points[f[2]][1]+y),(u_points[f[3]][0]+x, u_points[f[3]][1]+y)]        
            pygame.draw.polygon(screen,u_colors[i],pointlist)
            pointlist = [(u_points[f[0]][0]+x, u_points[f[0]][1]+y),(u_points[f[1]][0]+x, u_points[f[1]][1]+y),
                          (u_points[f[2]][0]+x, u_points[f[2]][1]+y),(u_points[f[3]][0]+x, u_points[f[3]][1]+y)]        
            pygame.draw.polygon(screen,(0,0,0),pointlist,1)
            i += 1

    def displayHeader(self):
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
        step = steps[self.currentStep]["step"]
        b_x = x_scale*820
        b_y = y_scale*10
        b_h = y_scale*30
		
        title = steps[self.currentStep]["title"]
        button(screen,"<<",ft_sz,b_x,b_y,x_scale*40,b_h,green,red,self.nextOrPrevious,-1)
        b_x += x_scale*70
        button(screen,step,ft_sz,b_x,b_y,x_scale*100,b_h,green,green)
        b_x += x_scale*120
        button(screen,title,ft_sz,b_x,b_y,x_scale*200,b_h,green,green)
        b_x += x_scale*230
        button(screen,">>",ft_sz,b_x,b_y,x_scale*40,b_h,green,red,self.nextOrPrevious,1)

    def displayTutorial(self):
        screen,ft_sz,x_scale,y_scale= getDisplayParams()
		
        step = steps[self.currentStep]["step"]
        title = steps[self.currentStep]["title"]
        texts = steps[self.currentStep]["text"]
        figures = steps[self.currentStep].get("figures",[])

        b_x = x_scale*820
        b_y = y_scale*45
        b_h = y_scale*28
        
        ln_size = y_scale*28
        if self.refresh == 1:
            pygame.draw.rect(screen,background,(b_x,b_y,x_scale*528,y_scale*635))
            self.refresh = 0
            line = 0
            for text in texts:
                printText(screen,text, "fangsong", ft_sz, b_x, b_y + b_h*line, white)
                line += 1
            b_x += x_scale*80
            b_y = y_scale*500
            offset = 0
            for fig in figures:
                self.displayFigure(screen, b_x+offset, b_y,figList[fig[0]][fig[1]])
                fig_label = u"图" + str(fig[0]+1)+ "-" + str(fig[1]+1)
                printText(screen,fig_label, "fangsong", ft_sz,  b_x+offset - x_scale*20, b_y + y_scale*65, white)
                offset += x_scale*120
    
              
