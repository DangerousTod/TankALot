import pygame, sys, os, math, numpy as np
class Cam:
    def __init__(self,pos=(0,0,0),center=(0,0,0),x=0,y=0,z=0):
	  self.pos = list(pos)
    def events(self,event):
    	pass
    def update(self,dt,key,rot):
    	s = dt*10
	    r = rot*36
		if key[pygame.K_s] and s != 1: self.pos[2]-=s   #forward
		else: self.pos[2] == 1
		if key[pygame.K_w]: self.pos[2]+=s   #back
		if key[pygame.K_q] and s != 1: self.pos[1]-=s   #up
		else: self.pos[1] == 1
		if key[pygame.K_e]: self.pos[1]+=s   #down
		if key[pygame.K_a] and s !=0: self.pos[0]-=s    #left
		else: self.pos[0] == 1
		if key[pygame.K_d]: self.pos[0]+=s   #right
class Cube:
    vertices = (-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)
    faces = (0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)
    colors = (255,0,0),(255,128,0),(255,255,0),(255,255,255),(0,0,255),(0,255,0)
    def __init__(self,pos=(1,1,1)):
		x,y,z = pos
		self.verts = [(x+X/2,y+Y/2,z+Z/2) for X,Y,Z in self.vertices]
pygame.init()
w,h = 800,600; cx,cy = w//2,h//2; fov = min(w,h)
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption('3D Graphics')
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()
cam = Cam((0,0,-5))
cubes = [Cube((0,0,0)),
Cube((-2,0,0)),Cube((2,0,0)),Cube((0,2,10)),Cube((0,0,10)),Cube((8,0,8)),
Cube((2,3,0)),Cube((-5,0,2)),Cube((5,0,3)),Cube((4,2,13)),Cube((7,8,10)),
Cube((9,9,0)),Cube((-9,0,4)),Cube((2,9,-11)),Cube((8,2,19)),Cube((9,0,19)),
Cube((-2,0,0)),Cube((2,0,0)),Cube((0,2,-10)),Cube((0,0,-10)),Cube((8,0,-8)),
Cube((2,-3,0)),Cube((-5,0,-2)),Cube((-5,0,-3)),Cube((4,2,-13)),Cube((7,8,-10)),
Cube((-9,-9,0)),Cube((-9,0,-4)),Cube((2,9,-11)),Cube((8,2,-19)),Cube((9,0,-19)),
Cube((-2,110,110)),Cube((112,10,10)),Cube((110,112,110)),Cube((110,0,110)),Cube((118,0,118)),
Cube((2,3,110)),Cube((-5,110,2)),Cube((115,0,3)),Cube((114,2,113)),Cube((17,8,110)),
Cube((119,19,10)),Cube((-19,10,14)),Cube((12,119,-111)),Cube((18,12,119)),Cube((19,110,119)),
Cube((-12,10,10)),Cube((12,110,10)),Cube((10,12,-110)),Cube((10,10,-110)),Cube((18,10,-18)),
Cube((12,-13,10)),Cube((-15,10,-12)),Cube((-15,10,-13)),Cube((14,12,-113)),Cube((17,18,-110)),
Cube((-19,-19,10)),Cube((-19,10,-14)),Cube((12,19,-111)),Cube((18,12,-119)),Cube((19,10,-119)),
Cube((8,8,8)),Cube((-7,4,5)),Cube((2,9,9)),Cube((0,6,10)),Cube((0,0,12))]
while True:
    dt = clock.tick()/1000
    rot = clock.tick()/1000
    r = rot*36
    for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
	    if event.key == pygame.K_x:
			datax = cam.pos[0]
			datay = cam.pos[1]
			for i in range(datax):
	        	for j in range(datay):
					cam.pos[0] = i * np.cos(r) - j * np.sin(r)
					cam.pos[1] = i * np.sin(r) - j * np.cos(r)
		if event.type == pygame.QUIT: pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
	    	if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
		cam.events(event)
    screen.fill((0,0,0))
    face_list = []; face_color = []; depth = []
    for obj in cubes:
		vert_list = []; screen_coords = []
		for x,y,z in obj.verts:
	  	  x-=cam.pos[0]; y-=cam.pos[1]; z-=cam.pos[2]
	      vert_list += [(x,y,z)]
	      f = fov/z; x,y = x*f,y*f
	      screen_coords+=[(cx+int(x),cy+int(y))]
		for f in range(len(obj.faces)):
	      face = obj.faces[f]
	      on_screen = False
	      for i in face:
		  	x,y = screen_coords[i]
		    if vert_list[i][2]>0 and x>0 and x<w and y>0 and y<h: on_screen = True; break
	    if on_screen:
			coords = [screen_coords[i] for i in face]
			face_list += [coords]
			face_color += [obj.colors[f]]
			depth += [sum(sum(vert_list[j][i] for j in face)**2 for i in range(3))]
    order = sorted(range(len(face_list)),key=lambda i:depth[i],reverse=1)
    print(order)
    for i in order:
		try: pygame.draw.polygon(screen,face_color[i],face_list[i])
	    except: pass
    pygame.display.flip()
    key = pygame.key.get_pressed()
    cam.update(dt,key,rot)
