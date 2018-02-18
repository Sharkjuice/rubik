#-*-coding:utf-8-*-
import pygame
from cubeGlobal import win_height,win_width,background,screen,black
#用一个全局变量表示鼠标状态，以判断鼠标点击（pressed，released）
mouse_pressed = 0    
def button(screen,msg,x,y,w,h,ic,ac,action=None,param=None):
    global mouse_pressed
    mouse = pygame.mouse.get_pos()
    mouse_status = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        mouse_current = mouse_status[0]
        if mouse_pressed == 1 and mouse_current == 0 and action != None:
            action(param)         
        mouse_pressed = mouse_current
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("kaiti",25)
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

def message(screen,text,x,y,color):
    largeText = pygame.font.SysFont('kaiti',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.left = x
    TextRect.top = y
    pygame.draw.rect(screen, color,TextRect)
    screen.blit(TextSurf, TextRect)

