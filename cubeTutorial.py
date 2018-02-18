#-*-coding:gbk-*-
import pygame
from cubeGlobal import background,screen,green,bright_green,colors
from cubeCommon import button,message,printText
steps = [
    {"step":u"ǰ��", "title":u"������ʶ",
    "text":[
u"1. ħ����6�棬6����ɫ���ܹ���27���飬",u"������8���ǿ飬12����飬6�����Ŀ顣",
u"ÿ���ǿ���3���棬�����2���棬 ����",u"����һ���档ת��ʱ������λ�ò��䡣",
u"2. ���ǰ�ħ���������ϣ���ǰ�������",u"��ΪF/f/B��(ͼ8-1������ǰ������ֱ�Ϊ",
u"R/r/L��(ͼ8-2������������ֱ�ΪU/u/D",u"�棨ͼ8-3����",
u"3. ���½ǰ�ť���ֱ��ʾת�����棬��Ʋ",u"�ı�ʾ��ʱ��ת������Ʋ��ʾ˳ʱ��ת��",
u"ÿ�β���������ת90�ȡ�"],
    "figures":[(7,0),(7,1),(7,2)]
     },
    {"step":u"��һ��", "title":u"�ײ�ʮ�ֻ�ԭ",
     "text":[
u"�ҵ���ɫ���Ŀ飬��Ϊ����, Ȼ���4����",u"�а�ɫ�������������棬�۲��ɫ����",
u"����ɫ,ת�������������Ӧ���Ŀ����(��",u"ͼ1-1)��4����ɫ���������档�������һ",
u"���ײ�ʮ�֣�����ʮ�ֲ�����ɫ�����Ŀ��",u"��(��ͼ1-3)������ɫ���ڶ�����Ҫ��תʱ,",
u"(ͼ1-2)ת��ʽ1: F R U"],
    "figures":[(0,0),(0,1),(0,2)]
    },    
    {"step":u"�ڶ���", "title":u"�׽ǹ�λ(1)",
     "text":[
u"��ԭħ����һ���ĸ��ǻ�����������:  ",
u"1. �ڶ������ҵ�һ���а�ɫ��Ľǿ�,ת",u"�����㣬���ǿ����ǰ�����Ͻ�λ��,�۲�",
u"�ǿ�����������ɫ,ת��ħ����������ֱ��",u"����ǰ����������Ŀ���ɫ���Ӧ(��ͼ2-1,",
u"2-2, 2-3)��ͼ2-1ʹ�ù�ʽ2-1��ͼ2-2ʹ",u"�ù�ʽ2-2��ͼ2-3ʹ�ù�ʽ2-3, ���",
u"���1����ʹ�ù�ʽ2-1��",u"��ʽ2-1��R U R' ��ʽ2-2: F' U' F",
u"��ʽ2-3Ϊ��RUU R'U'��" ],
     "figures":[(1,0),(1,1),(1,2)]
    },
    {"step":u"�ڶ���", "title":u"�׽ǹ�λ(2)",
     "text":[
u"2. ����ײ�û�и�ԭ������Ҳû�д���ɫ",u"��Ľǿ飬�۲�ײ��ҵ�λ�ô���Ľǿ飬",
u"����ǰ�����½�λ�ã���ͼ2-4��2-5), ͼ",u"2-4ʹ�ù�ʽ2-4���ͼ2-1��ͼ2-5ʹ�ù�",
u"ʽ2-5,���ͼ2-2�� �ٷֱ�ʹ��ǰ������", u"�Ϳ���ɡ�",
u"��ʽ2-4��RUR'U'�� ��ʽ2-5��F' U' F U��"],
     "figures":[(1,3),(1,4)]
    },
    {"step":u"������", "title":u"�в�����λ(1)",
     "text":[
u"������Ҫ�ڶ����ҵ�һ��û�л�ɫ�����飬",u"ת���ϲ㣬����������ɫ��������ɫ",
u"����,���ǰѶ��������涨��Ϊ���棬�۲�",u"����������ɫ����ʱ��������������",
u"1. ��ǰ�����Ŀ���ɫһ��(��ͼ3-1)����ʱ",u"��Ҫ�ù�ʽ3-1�������ܸ�λ��ǰ��λ�á�",
u"2. �����ǰ�����Ŀ���ɫ��һ��(��ͼ3-2)��",u"��Ҫ�ù�ʽ3-2�����ܸ�ԭ��������λ�á�",
u"��ʽ3-1��R'U'R'U'R' URUR(������˳) ",u"��ʽ3-2��RURUR U'R'U'R'(��˳����)"],
     "figures":[(2,0),(2,1)]
    },

    {"step":u"������", "title":u"�в�����λ(2)",
     "text":[
u"3. ������������в���������Ҫ������",u"��ʱ��Ҫ��������ǰ�������λ��(��ͼ",
u"3-3),ת����ʽ3-1���ܽ�����������㣬",u"�ٰ������1�����2�ķ���������ɡ�",
u"��ʽ3-1��R'U'R'U'R' URUR(������˳) ",u"��ʽ3-2��RURUR U 'R'U'R'(��˳����)"],
     "figures":[(2,2)]
    },

   {"step":u"���Ĳ�", "title":u"�����ʮ��",
     "text":[
u"������Ļ�ԭ��Ҫ�ڶ����һ����ɫ'ʮ��'",u"�ܡ��ڼ�ʮ�ֵ�ʱ��س������������",
u"1.�����Ѿ��л�ɫ������'һ'��(��ͼ4-1) ",u"��ʱ��Ҫת����ʽ4�����ܼӼܺö����ɫ",
u"ʮ�ּܡ�",
u"2.�����Ѿ��л�ɫ�������ֱ�ǣ�������λ",u"����ֱ��(��ͼ4-2)��ת����ʽ4���ͱ����",
u"��1���������1�ķ������ܽ�����ʮ�ּܺá�",
u"3.����ֻ��һ����ɫ���Ŀ�(��ͼ4-3)����ʱ",u"������Ҫ���ⷽ��ת��һ�ι�ʽ4��ת�����",
u"��2���������2�ķ������ܽ�����ʮ�ּܺá�",u"��ʽ4�� F R U R' U' F'"],
     "figures":[(3,0),(3,1),(3,2)]
    },
   {"step":u"���岽", "title":u"�������λ(1)",
     "text":[
u"��һ��������Ҫ�������ɫ���λ�������",u"���������",
u"1. ����ֻ��һ����ɫ�ǿ飬ת����������",u"ǰ��λ��(ͼ5-1)��ת����ʽ5������ɡ���",
u"û�и�ԭ���Ժýǿ�λ�ú����ظ�һ�ι�",u"ʽ5-1��������ɡ�",
u"��ʽ5-1��R' U2 RU R' UR"],
     "figures":[(4,0)]
    },    
   {"step":u"���岽", "title":u"�������λ(2)",
     "text":[
u"2. ������������ɫ�Ľǿ飬ת������ֱ��",u"��������Ͻǳ��ֻ�ɫ�ǿ���(��ͼ5-2��5-",
u"3��5-4),��ת����ʽ5�������1�������",u"1�ķ���������ɡ�",
u"��ʽ5-1��R' U2 RU R' UR"],
     "figures":[(4,1),(4,2),(4,3)]
    },
   {"step":u"���岽", "title":u"�������λ(3)",
     "text":[
u"3. ����û�л�ɫ�Ľǿ飬ת������ֱ��ǰ",u"�����Ͻ�λ�ó��ֻ�ɫ�ǿ���(��ͼ5-5)��",
u"ת����ʽ5-1�������1��",u"��ʽ5-1��R' UU RU R' UR",
u"��ʽ5-1�����ǶԽǻ����� ����һ�ǲ���(",u"�������Ͻǣ���������ԭ��˳ʱ����ת120",
u"���ٻ�λ�� ��˹۲죬�����Ҫ��ʱ����", u"���������湫ʽ��",
u"��ʽ5-2��F UU F' U' F U' F'"],
     "figures":[(4,4)]
    },
    
   {"step":u"������", "title":u"���ǹ�λ",
     "text":[
u"�������нǿ��������ȷλ�õ�ʱ��س���",u"���������",
u"1. �ڶ�������ҵ���������ͬ��ɫ�Ľǿ飬",u"����һ�涨λΪǰ��(��ͼ6-1)��ת����ʽ6",
u"������ɡ�",
u"2. ���������û���ҵ�������ͬ��ɫ�Ľ�",u"��(��ͼ6-2)��ת����ʽ6�ͻ������1��",
u"��ʽ6��Lr' U' R D2 R' UR D2 R2",    u"��ʽ6��������������ʱ�뻥�����������Ͻ�",
u"�������ƶ���"],
     "figures":[(5,0),(5,1)]
    },    
   {"step":u"���߲�", "title":u"�����λ",
     "text":[
u"�ڶ����λʱ��������������",
u"1. �����ĸ�����У���һ���Ѿ�������ȷ",u"λ��, ���ǰ���һ�涨Ϊ����(��ͼ7-1)",
u"��ת����ʽ7-1 һ�λ����μ�����ɡ�",
u"2. ������û���������ȷ��λ��(��ͼ7-2)",u"ת����ʽ7�ͻ������1��",
u"��ʽ7��R2 U' f' U2 f U' R'2",          u"��ʽ7-1����������������ʱ�뻥�������",
u"��Ҫʹ�����ι�ʽ����ʱ�����ʹ�ù�ʽ7-",u"2����ʵ����ʱ�뻥������ֻ��Ҫʹ��һ��",
u"��ʽ7-2��F2 U r U2 r�� U F2"],
     "figures":[(6,0),(6,1)]
    }    
]

figList = [
   
#��1��
[("---gbwwww","---rr----","-wwwyw-ww"),
("---wb----","---rr----","-b-wyw-w-"),
("---rr----","---bb----","-w-www-w-")],
#��2��
[("b---bb--b","w---rr--r","r--------"),
("w---bb--b","r---rr--r","b--------"),
("r---bb--b","b---rr--r","w--------"),
("--r-bb--b","--w-rr--r","---------"),
("--w-bb--b","--b-rr--r","---------")],
#��3��
[("--b-bb-bb","--rrrr-rr","---by----"),
("--b-bb-bb","--rrrr--r","---gy----"),
("-rb-bb-bb","-br-rr-rr","----y----")],
#��4��
[
("-bbybb-bb","-rr-rr-rr","---yyy---"),
("-bbybb-bb","-rryrr-rr","----yy-y-"),
("-bbybb-bb","-rryrr-rr","----y----")],
#��5��
[("-bb-bb-bb","-rr-rr-rr","yy-yyy-y-"),
("-bb-bb-bb","yrr-rr-rr","-yyyyyyy-"),
("-bb-bb-bb","yrr-rr-rr","-y-yyyyyy"),
("-bb-bb-bb","yrr-rryrr","-yyyyy-yy"),
("ybb-bb-bb","-rr-rr-rr","-y-yyy-y-")],
#��6��
[("gbb-bbgbb","-rr-rr-rr","yyyyyyyyy"),
("bbb-bbgbb","rrr-rrorr","yyyyyyyyy")],
#��7��
[("bbb-bbbbb","rrrgrrrrr","yyyyyyyyy"),
("bbb-bbbbb","rrrgrrrrr","yyyyyyyyy")],
#��0��
[("---------","yyyrrrggg","yyyrrrggg"),
("yyyrrrggg","---------","yrgyrgyrg"),
("yrgyrgyrg","yrgyrgyrg","---------")],
] 

currentStep = 0
refresh = 1
def nextOrPrevious(isNext):
    global currentStep,refresh
    currentStep += isNext
    refresh = 1
    if currentStep < 0:
        currentStep = 0
    elif currentStep > 11:
        currentStep = 11
    


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

def displayFigure(screen,x,y,figure):
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
def displayTutorial(screen):
    global refresh
    step = steps[currentStep]["step"]
    title = steps[currentStep]["title"]
    button(screen,"<<",810,10,40,30,green,bright_green,nextOrPrevious,-1)
    button(screen,step,880,10,100,30,green,green)
    button(screen,title,1000,10,200,30,green,green)
    button(screen,">>",1230,10,40,30,green,bright_green,nextOrPrevious,1)
    
 
    texts = steps[currentStep]["text"]
    figures = steps[currentStep].get("figures",[])
    if refresh == 1:
        pygame.draw.rect(screen,background,(810,45,500,555))
        refresh = 0
        line = 0
        for text in texts:
            printText(screen,text, "kaiti", 25, 810, 45+28*line, (240,240,240))
            line += 1
        x = 880
        y = 500
        offset = 0
        for fig in figures:
            displayFigure(screen,x+offset,y,figList[fig[0]][fig[1]])
            fig_label = u"ͼ" + str(fig[0]+1)+ "-" + str(fig[1]+1)
            printText(screen,fig_label, "kaiti", 25, x + offset - 20, y + 65, (200,200,200))
            offset += 120
    
              
