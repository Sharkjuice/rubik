#-*-coding:utf-8-*-
import pygame
from cubeGlobal import black,mouse_status
#用一个全局变量表示鼠标状态，以判断鼠标点击（pressed，released）
mouse_pressed = 0  
def button(screen,msg,Textsize,x,y,w,h,ic,ac,action=None,param=None):
    global mouse_status
    mouse_current = mouse_status[0]

    if x+w > mouse_status[1] > x and y+h > mouse_status[2] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        mouse_current = mouse_status[0]
        if mouse_current == 1 and action != None:
            action(param)
        mouse_status[0] = 0
        mouse_status[1] = 0
        mouse_status[2] = 0
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("fangsong",Textsize)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def printText(screen,txtText, Textfont, Textsize , Textx, Texty, Textcolor):
	# pick a font you have and set its size
	myfont = pygame.font.SysFont(Textfont, Textsize)
	# apply it to text on a label
	label = myfont.render(txtText, 1, Textcolor)
	# put the label object on the screen at point Textx, Texty
	screen.blit(label, (Textx, Texty))
	# show the whole thing
	#pygame.display.flip()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()



