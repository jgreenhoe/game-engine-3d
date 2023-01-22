#Variable for setting color of shapes
red = (225,0,0)
black = (0,0,0)
blue = (0,0,225)
green = (0,225,0)
pink = (255,192,203)
orange = (255,165,0)
purple = (216,191,216)

import math
import copy
import time
#Initializing pygame
import pygame
pygame.init()
screen = [1915,1000]
surface = pygame.display.set_mode(screen)
surface.fill(black)
#Declaring lists and variables
d = 500
    #points of initial shape
rect = [[[-50, -50, 50], [-50, 50, 50], [50, 50, 50], [50, -50, 50], [-50, -50, -50], [-50, 50, -50], [50, 50, -50], [50, -50, -50]],[100,100,100]]
rect_c = [[[0,1,2,3],red],[[4,5,6,7],pink],[[0,3,7,4],green],[[1,2,6,5],orange],[[0,1,5,4],blue],[[2,3,7,6],blue]]
tri = [[0, 50, 0,[1,1]], [-50, -50, -50,[2,2]], [50, -50, -50,[2,3]], [0, -50, 50,[2,4]], [-50, -50, -50,[3,2]], [50, -50, -50,[3,3]], [0, -50, 50,[3,4]]]
pos = [0,0,-300]
comp = []
right = 0
up = 0
forw = 0
cam = [0,0,0]
cam_right = 0
cam_up = 0
font = pygame.font.SysFont('lato',20,True)

def flatten(points_d):
    t = []
    for i in range(0,len(points_d)):
        for p in range(0,len(points_d[i][2])):
            s = points_d[i][2][p][0][0]
            for m in range(0,len(points_d[i][2][p][0])):
                new0 = points_d[i][1][points_d[i][2][p][0][m]]
                old0 = points_d[i][1][s]
                dist_new0 = math.sqrt((new0[0]-pos[0])**2 + (new0[1]-pos[1])**2 + (new0[2]-pos[2])**2)
                dist_old0 = math.sqrt((old0[0]-pos[0])**2 + (old0[1]-pos[1])**2 + (old0[2]-pos[2])**2)
                if dist_new0 > dist_old0:
                    s = points_d[i][2][p][0][m]
            t.append([i,p,s])
    points = []
    far = 0
    len_t = len(t)
    for p in range(0,len_t):
        far = 0
        for i in range(0,len(t)):
            new1 = points_d[t[i][0]][1][t[i][2]]
            old1 = points_d[t[far][0]][1][t[far][2]]
            if math.sqrt((new1[0]-pos[0])**2 + (new1[1]-pos[1])**2 + (new1[2]-pos[2])**2)>math.sqrt((old1[0]-pos[0])**2 + (old1[1]-pos[1])**2 + (old1[2]-pos[2])**2):
                far = i
        points.append([[]])
        for n in points_d[t[far][0]][2][t[far][1]][0]:
            points[p][0].append(points_d[t[far][0]][1][n])
        points[p].append(points_d[t[far][0]][2][t[far][1]][1])
        t.remove(t[far])
#Converting 3d shapes into 2d
    flat = []
    count = 0
    for p in points:
        flat.append([[]])
        for i in p[0]:
            if i[2] != pos[2]:
                coord = [(i[0]-pos[0])/(i[2]-pos[2])*d,-(i[1]-pos[1])/(i[2]-pos[2])*d]
            else:
                coord = [(i[0]-pos[0])/((i[2]-pos[2]+1)/d),-(i[1]-pos[1])/((i[2]-pos[2]+1)/d)]
            coord[0]+=screen[0]/2
            coord[1]+=screen[1]/2
            flat[count][0].append(coord)
        flat[count].append(p[1])
        count+=1
#Drawing shapes
    for i in range(0,len(flat)):
        check = True
        for p in range(0,len(flat[i][0])):
            if points[i][0][p][2]<pos[2]:
                check = False
        if check == True:
            pygame.draw.polygon(surface,flat[i][1],flat[i][0])
#shape format [[x,y,z],[x,y,z]...] point format [x,y,z] theta format [x,y,z]
def rotate(shape,point,theta):
    for i in shape:
        cos = math.cos(theta[1])
        sin = math.sin(theta[1])
        x = i[0]-point[0]
        z = i[2]-point[2]
        i[0] = x*cos-z*sin+point[0]
        i[2] = z*cos+x*sin+point[2]
        
        cos = math.cos(theta[0])
        sin = math.sin(theta[0])
        y = i[1]-point[1]
        z = i[2]-point[2]
        i[1] = y*cos-z*sin+point[1]
        i[2] = z*cos+y*sin+point[2]
        
        cos = math.cos(theta[2])
        sin = math.sin(theta[2])
        x = i[0]-point[0]
        y = i[1]-point[1]
        i[0] = x*cos-y*sin+point[0]
        i[1] = y*cos+x*sin+point[1]

#point_o format [x,y,z] shape format [[x,y,z],[size_x,size_y,size_z],[tilt_x,tilt_y,tilt_z]]
def hitbox(point_o,shape):
    point = copy.deepcopy(point_o)
    rotate([point],shape[0],[-shape[2][0],-shape[2][1],-shape[2][2]])
    point[0] -= shape[0][0]
    point[1] -= shape[0][1]
    point[2] -= shape[0][2]
    xy = abs(point[0]/(shape[1][0]/2)+point[1]/(shape[1][1]/2))+abs(point[0]/(shape[1][0]/2)-point[1]/(shape[1][1]/2)) <= 2
    xz = abs(point[0]/(shape[1][0]/2)+point[2]/(shape[1][2]/2))+abs(point[0]/(shape[1][0]/2)-point[2]/(shape[1][2]/2)) <= 2
    if xy & xz:
        return True
    else:
        return False
def create_shape(x,y,z,shape,colors,size_x=1,size_y=1,size_z=1,tilt_x=0,tilt_y=0,tilt_z=0):
    name = []
    hitbox = []
    name.append([x,y,z])
    name.append([])
    for i in shape[0]:
        name[1].append([i[0]*size_x,i[1]*size_y,i[2]*size_z])
    rotate(name[1],[0,0,0],[tilt_x,tilt_y,tilt_z])
    name.append(colors)
    name.append([name[0],shape[1],[tilt_x,tilt_y,tilt_z]])
    return name

s = create_shape(0,0,500,rect,rect_c)
s1 = create_shape(500,0,500,rect,rect_c,3,3,1,4)
s2 = create_shape(-200,0,-40,rect,rect_c,2,1,2,0,0,2)
s3 = create_shape(500,0,0,rect,rect_c)
player = create_shape(pos[0],pos[1],pos[2]+10,rect,rect_c,.1,.1,.1,math.pi/4,math.pi/4)

def move(*shapes):
    global right
    global up
    global forw
    global cam_right
    global cam_up
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right -= 5
            if event.key == pygame.K_a:
                right += 5
            if event.key == pygame.K_SPACE:
                up -= 5
            if event.key == pygame.K_LSHIFT:
                up += 5
            if event.key == pygame.K_w:
                forw -= 5
            if event.key == pygame.K_s:
                forw += 5
            if event.key == pygame.K_RIGHT:
                cam_right -= 0.1
            if event.key == pygame.K_LEFT:
                cam_right += 0.1
            if event.key == pygame.K_UP:
                cam_up -= 0.1
            if event.key == pygame.K_DOWN:
                cam_up += 0.1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right += 5
            if event.key == pygame.K_a:
                right -= 5
            if event.key == pygame.K_SPACE:
                up += 5
            if event.key == pygame.K_LSHIFT:
                up -= 5
            if event.key == pygame.K_w:
                forw += 5
            if event.key == pygame.K_s:
                forw -= 5
            if event.key == pygame.K_RIGHT:
                cam_right += 0.1
            if event.key == pygame.K_LEFT:
                cam_right -= 0.1
            if event.key == pygame.K_UP:
                cam_up += 0.1
            if event.key == pygame.K_DOWN:
                cam_up -= 0.1
    cam[1]+=cam_right
    cam[0]+=cam_up
    if cam[1]>(math.pi*2):
        cam[1]-=(math.pi*2)
    if cam[1]<0:
        cam[1]+=(math.pi*2)
    if cam[0]>=math.pi/2:
        cam[0]=math.pi/2
    if cam[0]<=-math.pi/2:
        cam[0]=-math.pi/2

def exec_world(*shapes):
    m = []
#    for points in shapes:
#        for i in player[1]:
#            print(hitbox(i,points[3]))
    for points in shapes:
        r = copy.deepcopy(points)
        for i in r[1]:
            for c in range(0,len(i)):
                i[c]+=r[0][c]
        rotate(r[1],pos,cam)
        m.append(r)
    for i in m:
        comp.append(i)
    
def exec_player(*shapes):
#    for points in shapes:
#        for i in player[1]:
#            print(hitbox(i,points[3]))
    for points in shapes:
        r = copy.deepcopy(points)
        for i in r[1]:
            for c in range(0,len(i)):
                i[c]+=r[0][c]
    comp.append(r)
        
while True:
    start = time.time()
    surface.fill(black)
    player[0][0] = pos[0]
    player[0][1] = pos[1]-20
    player[0][2] = pos[2]+60
    comp = []
    exec_player(player)
    exec_world(s,s1,s2,s3)
    flatten(comp)
    move()
    pos[0]+=math.cos(cam[1])*right
    pos[2]-=math.sin(cam[1])*right
    pos[1]+=up
    pos[2]+=math.cos(cam[1])*forw
    pos[0]+=math.sin(cam[1])*forw
    loc_t = font.render('pos: '+str(int(pos[0]))+', '+str(int(pos[1]))+', '+str(int(pos[2])),True,red)
    surface.blit(loc_t,(0,0))
    pygame.display.update()
    end = time.time()
    if end-start < .017:
        time.sleep(.017-(end-start))