#!/usr/bin/env python
from pygame.locals import *
import pygame,time
from sys import *
from random import *
from os import listdir,putenv,getenv
from os.path import exists
from espeak import espeak

def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])

###############################################################################
# Utility Code
###############################################################################

def pick(lower=0,upper=255):
	return (randint(lower,upper),randint(lower,upper),randint(lower,upper))


def cls(a=0,b=0,c=0):
	display.fill([a,b,c])
	pygame.display.flip()


def print_at(dx,dy,msg,size=0,color=(255,255,255),bcolor=None):
	if size==0:
		size=int(y/5)
	fnt=pygame.font.Font(None,size)
	txt=fnt.render(msg,True,color)
	if txt.get_width()<x:
		x_scale=(x-txt.get_width())/2
		y_scale=(y-txt.get_height())/2
		x_rend=(dx+1)*x_scale
		y_rend=(dy+1)*y_scale
		if bcolor:
			txtb=fnt.render(msg,True,bcolor)
			for ox in xrange(-6,9,3):
				for oy in xrange(-6,9,3):			
					display.blit(txtb,(x_rend+ox,y_rend+oy))
		display.blit(txt,(x_rend,y_rend))
		pygame.display.flip()


def say(obj):
	snd="Resources/Words/%s.wav" % (obj)
	if exists(snd):
		pygame.mixer.stop()
		noise=pygame.mixer.Sound(snd)
		noise.play()
	else:
		pygame.mixer.stop()
		try:
			espeak.core.synth(obj)
		except:
			pass
			
			
def sound(obj):
	for tryit in [ obj, obj[:-1], obj+'s' ]:
		snd="Resources/Sounds/%s.wav" % (tryit)
		if exists(snd):
			pygame.time.wait(1000)
			pygame.mixer.stop()
			snd=pygame.mixer.Sound(snd)
			snd.play()
			
			
def picture(filename):
	pic=pygame.image.load(filename)
	ix,iy = pic.get_size()
	if ix > iy:
		# fit to width
		scale_factor = x/float(ix)
		sy = scale_factor * iy
		if sy > y:
			scale_factor = y/float(iy)
			sx = scale_factor * ix
			sy = y
		else:
			sx = x
	else:
		# fit to height
		scale_factor = y/float(iy)
		sx = scale_factor * ix
		if sx > x:
			scale_factor = x/float(ix)
			sx = x
			sy = scale_factor * iy
		else:
			sy = y
	pic=pygame.transform.smoothscale(pic,(int(sx),int(sy)))
	display.blit(pic,((x-pic.get_width())/2,(y-pic.get_height())/2))
	pygame.display.flip()


###############################################################################
# Game Code
###############################################################################
def splash():
	cls(*pick(128,192))
	print_at(0,-0.85,"Words",size=int(y/3),color=pick(64,128),bcolor=pick(0,64))
	pygame.time.wait(500)
	print_at(0,-0.25,"And",size=int(y/3),color=pick(64,128),bcolor=pick(0,64))
	pygame.time.wait(500)
	print_at(0,0.3,"Pictures",size=int(y/3),color=pick(64,128),bcolor=pick(0,64))
	pygame.time.wait(500)
	print_at(0,0.97,"(c) N. Garnett 2013",size=int(y/10),color=pick(192,255),bcolor=pick(0,64))
	pygame.time.wait(500)


def get_button():
	button=None
	while button==None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit(0)
			if event.type == pygame.KEYDOWN:
				button=event.key
				#if button==pygame.K_ESCAPE:
				#	pygame.quit()
				#	exit(0)
			if event.type == pygame.MOUSEBUTTONDOWN:
				#(a,b,c)=pygame.moouse.get_pressed()
				pygame.quit()
				exit(0)
	return (button)


def press_keys():
	c=None
	b=get_button()
	shown={}
	while b!=pygame.K_ESCAPE:
		if (b in xrange(97,123)) or (b in xrange(48,59)):
			c=chr(b).upper()
			if c=='0': c='10'
			files=listdir("Resources/"+c+"/")
			if not shown.has_key(c): shown[c]=[]
			if len(shown[c])==len(files): shown[c]=[]
			a_file=choice(files)
			while a_file in shown[c]: a_file=choice(files)
			shown[c].append(a_file)
			a_path="Resources/"+c+"/"+a_file

			cls(*pick(0,255))
			print_at(0,0,c,size=y,color=pick(128,255),bcolor=pick(0,128))
			say(c)
			pygame.time.wait(800)

			cls()
			picture(a_path)
			msg=a_file[:-4]
			if c<'A': msg=c+" "+msg
			print_at(0,0.8,msg,size=150,color=(255,255,0),bcolor=(0,0,0))	
			say(a_file[:-4])
			sound(a_file[:-4])				
			
			b=get_button()


###############################################################################
# Initialisation Code
###############################################################################
pygame.mixer.pre_init(48000,-16,2,4096)
try:
	getenv('DISPLAY')
except:
	putenv('SDL_VIDEODRIVER', 'fbcon')
pass
pygame.init()
dobj=pygame.display.Info()
y=dobj.current_h
x=dobj.current_w
display=pygame.display.set_mode((x,y),FULLSCREEN)
pygame.mouse.set_visible(False)


###############################################################################
# Main Loop
###############################################################################
while True:
	splash()
	press_keys()

