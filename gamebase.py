#Variable for setting color of shapes
red = (225,0,0)
black = (0,0,0)

import math
import copy
import time
#Initializing pygame
import pygame
pygame.init()
screen = [1900,1000]
surface = pygame.display.set_mode(screen)
surface.fill(black)
#Declaring lists and variables
d = 500
    #points of initial shape
rect = [[-50, -50, 50,[2,2]], [-50, 50, 50,[3,3]], [50, 50, 50,[4,1]], [50, -50, 50,[3,4]], [-50, -50, -50,[1,1]], [-50, 50, -50,[2,4]], [50, 50, -50,[3,2]], [50, -50, -50,[2,3]]]
tri = [[0, 50, 0,[1,1]], [-50, -50, -50,[2,2]], [50, -50, -50,[2,3]], [0, -50, 50,[2,4]], [-50, -50, -50,[3,2]], [50, -50, -50,[3,3]], [0, -50, 50,[3,4]]]
pos = [0,0,-300]
left = False
right = False
up = False
down = False
forw = False
back = False
cam = [0,0]
cam_left = False
cam_right = False
cam_up = False
cam_down = False
font = pygame.font.SysFont('lato',20,True)

def flatten(points):
#Converting 3d shapes into 2d
    flat = []
    for i in range(0,len(points)):
        if points[i][2] != pos[2]:
            flat.append([(points[i][0]-pos[0])/((points[i][2]-pos[2])/d),-(points[i][1]-pos[1])/((points[i][2]-pos[2])/d),points[i][3]])
        else:
            flat.append([(points[i][0]-pos[0])/((points[i][2]-pos[2]+1)/d),-(points[i][1]-pos[1])/((points[i][2]-pos[2]+1)/d),points[i][3]])
        flat[i][0]+=screen[0]/2
        flat[i][1]+=screen[1]/2
        flat[i][0] = round(flat[i][0],5)
        flat[i][1] = round(flat[i][1],5)
#Connecting points
    for i in range(0,len(flat)):
        for p in range(0,len(flat)):
            if (flat[i][2][0] == flat[p][2][0]+1) & (flat[i][2][1] != flat[p][2][1]):
                if (pos[2]<points[i][2]) & (pos[2]<points[p][2]):
                    try:
                        pygame.draw.line(surface,red,flat[i][0:2],flat[p][0:2])
                    except:
                        flat = flat

def rotate(shape):
    points = create_shape(*shape)
    r = copy.deepcopy(points)
    for i in range(0,len(r)):
        cos = math.cos(cam[1])
        sin = math.sin(cam[1])
        x = r[i][0]-pos[0]
        z = r[i][2]-pos[2]
        r[i][0] = x*cos-z*sin+pos[0]
        r[i][2] = z*cos+x*sin+pos[2]

        cos = math.cos(cam[0])
        sin = math.sin(cam[0])

        y = r[i][1]-pos[1]
        z = r[i][2]-pos[2]
        r[i][1] = y*cos-z*sin+pos[1]
        r[i][2] = z*cos+y*sin+pos[2]

    flatten(r)

def create_shape(x,y,z,shape,size_x=1,size_y=1,size_z=1,tilt_x=0,tilt_y=0,tilt_z=0):
    name = []
    hitbox = []
    xmin = x
    xmax = x
    ymin = y
    ymax = y
    zmin = z
    zmax = z
    if shape == 'rect':
        shape = rect
    elif shape == 'tri':
        shape = tri
    else:
        raise TypeError('invalid shape argument')
    for i in range(0,len(shape)):
        name.append(([x+shape[i][0]*size_x,y+shape[i][1]*size_y,z+shape[i][2]*size_z,shape[i][3]]))
        if shape[i][0]>xmax:
            xmax = shape[i][0]
        if shape[i][0]<xmin:
            xmin = shape[i][0]
        if shape[i][1]>ymax:
            ymax = shape[i][1]
        if shape[i][1]<ymin:
            ymin = shape[i][1]
        if shape[i][2]>zmax:
            zmax = shape[i][2]
        if shape[i][2]<zmin:
            zmin = shape[i][2]
        
        cos = math.cos(tilt_y)
        sin = math.sin(tilt_y)
        rx = name[i][0]-x
        rz = name[i][2]-z
        name[i][0] = rx*cos-rz*sin+x
        name[i][2] = rz*cos+rx*sin+z
        
        cos = math.cos(tilt_x)
        sin = math.sin(tilt_x)
        ry = name[i][1]-y
        rz = name[i][2]-z
        name[i][1] = ry*cos-rz*sin+y
        name[i][2] = rz*cos+ry*sin+z
        
        cos = math.cos(tilt_z)
        sin = math.sin(tilt_z)
        rx = name[i][0]-x
        ry = name[i][1]-y
        name[i][0] = rx*cos-ry*sin+x
        name[i][1] = ry*cos+rx*sin+y
        
    hitbox = xmin<pos[0]<xmax & ymin<pos[1]<ymax & zmin<pos[2]<zmax
    return name

s0 = [0,0,500,'rect']
s1 = [500,0,500,'rect',3,3,1,4]
s2 = [-200,0,-40,'rect',2,1,2,0,0,2]
s3 = [500,0,0,'rect']

def move(*shapes):
    global left
    global right
    global up
    global down
    global forw
    global back
    global cam_left
    global cam_right
    global cam_up
    global cam_down
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                left = True
            if event.key == pygame.K_a:
                right = True
            if event.key == pygame.K_LSHIFT:
                up = True
            if event.key == pygame.K_SPACE:
                down = True
            if event.key == pygame.K_w:
                forw = True
            if event.key == pygame.K_s:
                back = True
            if event.key == pygame.K_RIGHT:
                cam_left = True
            if event.key == pygame.K_LEFT:
                cam_right = True
            if event.key == pygame.K_DOWN:
                cam_up = True
            if event.key == pygame.K_UP:
                cam_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                left = False
            if event.key == pygame.K_a:
                right = False
            if event.key == pygame.K_LSHIFT:
                up = False
            if event.key == pygame.K_SPACE:
                down = False
            if event.key == pygame.K_w:
                forw = False
            if event.key == pygame.K_s:
                back = False
            if event.key == pygame.K_RIGHT:
                cam_left = False
            if event.key == pygame.K_LEFT:
                cam_right = False
            if event.key == pygame.K_DOWN:
                cam_up = False
            if event.key == pygame.K_UP:
                cam_down = False
    if left == True:
        pos[0]+=math.cos(cam[1])*5
        pos[2]-=math.sin(cam[1])*5
    if right == True:
        pos[0]-=math.cos(cam[1])*5
        pos[2]+=math.sin(cam[1])*5
    if up == True:
        pos[1]-=5
    if down == True:
        pos[1]+=5
    if forw == True:
        pos[2]+=math.cos(cam[1])*5
        pos[0]+=math.sin(cam[1])*5
    if back == True:
        pos[2]-=math.cos(cam[1])*5
        pos[0]-=math.sin(cam[1])*5
    for points in shapes:
        if cam_left == True:
            cam[1]+=0.03
        if cam_right == True:
            cam[1]-=0.03
        if cam_up == True:
            cam[0]-=0.03
        if cam_down == True:
            cam[0]+=0.03
    if cam[1]>(math.pi*2):
        cam[1]-=(math.pi*2)
    if cam[1]<0:
        cam[1]+=(math.pi*2)
    if cam[0]>=math.pi/2:
        cam[0]=math.pi/2
    if cam[0]<=-math.pi/2:
        cam[0]=-math.pi/2
    surface.fill(black)
    for points in shapes:
        rotate(points)
        
while True:
    start = time.time()
    move(s0,s1,s2,s3)
    loc_t = font.render('pos: '+str(int(pos[0]))+', '+str(int(pos[1]))+', '+str(int(pos[2])),True,red)
    surface.blit(loc_t,(0,0))
    pygame.display.update()
    end = time.time()
    if end-start < .017:
        time.sleep(.017-(end-start))