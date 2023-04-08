#RGB color variables
red = [225,0,0]
black = [0,0,0]
blue = [0,0,225]
green = [0,225,0]
pink = [255,192,203]
orange = [255,165,0]
purple = [216,191,216]

import math
import random
import numpy as np
import time
import ctypes.util
import pynput
import threading
#Initializing pygame
import pygame
pygame.init()
screen = [1915,1000]
#surface = pygame.display.set_mode(screen)
#pygame.display.set_caption("Game Base")
#Declaring lists and variables
d = 500
#pos = [0,0,-10]
#vel_x = 0
#vel_y = 0
#vel_z = 0
#cam = [0,0,0]
#cam_vel_x = 0
#cam_vel_y = 0
#font = pygame.font.SysFont('lato',20,True)
drawPolygon = ctypes.PyDLL("/home/pi/drawPolygons.so")
def read_obj(obj_file):
    points = []
    shapes = []
    with open(obj_file) as file:
        for line in file:
            if line[:2] == "v ":
                x = line.find(" ") + 1
                y = line.find(" ",x) + 1
                z = line.find(" ",y) + 1
                points.append([float(line[x:y]),float(line[y:z]),float(line[z:-1])])
            elif line[0] == 'f':
                fline = []
                f_item = []
                space_start = 0
                more_face_values = True
                while more_face_values:
                    space_start = line.find(" ", space_start+1)
                    if (space_start == -1) or (line[space_start+1] == "\n"):
                        more_face_values = False
                    else:
                        slash_end = line.find("/",space_start)
                        if slash_end != -1:
                            f_item.append(int(line[space_start+1:slash_end]))
                        else:
                            space_end = line.find(" ", space_start+1)
                            f_item.append(int(line[space_start+1:space_end]))
                            space_start = space_end
                shapes.append(f_item)
    return [points,shapes]

class shapes:
    def __init__(self,obj_file):
        obj = read_obj(obj_file)
        self.points = np.array(obj[0])
        max_len = 3
        for i in obj[1]:
            if len(i) > max_len:
                max_len = len(i)
        for i in obj[1]:
            while len(i) < max_len:
                i.append(i[2])
        self.shapes = np.array(obj[1])
#multiplies self.shape by size
    def set_size(self,size):
        for i in self.points:
            i[0] = i[0]*size[0]
            i[1] = i[1]*size[1]
            i[2] = i[2]*size[2]
#takes variables to be used in tilt()
    def set_tilt(self,point,theta):
        self.point = point
        self.theta = theta
        self.ttheta = copy.deepcopy(theta)
#rotates self.coord by variable from set_tilt()
    def tilt(self):
        rotate(self.coord,self.point,self.theta)

class position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = -10
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0
        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = 0
        self.rt_x = 0
        self.rt_y = 0
        self.rt_z = 0
        self.pos = [self.x, self.y, self.z]
        self.cam = [self.cam_x, self.cam_y, self.cam_z]
    def update(self):
        self.x = self.x + self.vel_x
        self.y = self.y + self.vel_y
        self.z = self.z + self.vel_z
        self.cam_x = self.cam_x + self.rt_x
        self.cam_y = self.cam_y + self.rt_y
        self.cam_z = self.cam_z + self.rt_z
        self.pos = [self.x, self.y, self.z]
        self.cam = [self.cam_x, self.cam_y, self.cam_z]
    def right(self,a,cam_y):
        self.vel_x += math.cos(cam_y)*a
        self.vel_z += math.sin(cam_y)*a
    def forw(self,a,cam_y):
        self.vel_x += math.sin(cam_y)*a
        self.vel_z += math.cos(cam_y)*a
    def up(self,a):
        self.vel_y += a
position = position()
#turns objects of class shape into 2d points and draws it
def draw_points(points,faces):
#organize shapes by distance to pos
#shapes farthest away are drawn first
    start = time.time()
    rotated_points = rotate(points,position.pos,position.cam)
    if np.any((rotated_points[:,2] > position.pos[2])):
        point_is_onscreen = rotated_points[:,2] > position.pos[2]
        onscreen_points = rotated_points[point_is_onscreen]
        flat = np.array((500*(rotated_points[:,0]-position.pos[0])/(rotated_points[:,2]-position.pos[2])+screen[0]/2,-500*(rotated_points[:,1]-position.pos[1])/(rotated_points[:,2]-position.pos[2])+screen[1]/2))
        faces_array = np.array(faces)
        flat = np.swapaxes(flat,0,1)
        shaped_points = flat[faces_array-1]
        point_is_onscreen = point_is_onscreen[faces_array-1]
        sort_points = np.linalg.norm(rotated_points[faces_array[:,0]-1]-position.pos,axis=1)
        sort_index = np.argsort(sort_points)
        shaped_points = shaped_points[np.flip(sort_index)]
        point_is_onscreen = point_is_onscreen[np.flip(sort_index)]
        shaped_points = np.ascontiguousarray(np.swapaxes(shaped_points,1,2))
#        shaped_points = np.array([[[0,0,50,50],[0,50,50,0]],[[0,0,50,50],[0,50,50,0]],[[0,0,50,50],[0,50,50,0]]])
        end = time.time()
#        print(end-start)
        count = 0
        r = 0
        g = 0
        b = 0
        start = time.time()
#        for i in shaped_points:
#            if len(i) > 2 and np.all(point_is_onscreen[count]):
#                pygame.draw.polygon(surface,(r,g,b,17),i)
        
        shaped_points = shaped_points.astype(np.int32)
        shaped_points_ptr = shaped_points.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        draw_polygon = draw_loop(window,renderer,shaped_points.shape[0],shaped_points.shape[2],shaped_points_ptr)
        print(" ")
#            r += .03
#            g += .03
#            b += .03
#            count += 1
        end = time.time()
#        print(end-start)
#rotates shape around points by theta
#shape format [[x,y,z],[x,y,z]...] point format [x,y,z] theta format [x,y,z]
def rotate(shape,point,theta):
    sc = np.copy(shape)
    
    cos = np.cos(theta[1])
    sin = np.sin(theta[1])
    x = sc[:,0]-point[0]
    z = sc[:,2]-point[2]
    sc[:,0] = x*cos-z*sin+point[0]
    sc[:,2] = z*cos+x*sin+point[2]
    
    cos = np.cos(theta[0])
    sin = np.sin(theta[0])
    y = sc[:,1]-point[1]
    z = sc[:,2]-point[2]
    sc[:,1] = y*cos-z*sin+point[1]
    sc[:,2] = z*cos+y*sin+point[2]
    
    cos = np.cos(theta[2])
    sin = np.sin(theta[2])
    x = sc[:,0]-point[0]
    y = sc[:,1]-point[1]
    sc[:,0] = x*cos-y*sin+point[0]
    sc[:,1] = y*cos+x*sin+point[1]
    
    return sc

#determines if any points of shape2 is inside rectangular hitbox of shape1
def hitbox(shape1,shape2):
    #shape1_c and shape2_c are expendible copies of shape1 and shape2, to be manipulated without changing actual objects
    shape1_c = copy.deepcopy(shape1)
    shape2_c = copy.deepcopy(shape2)
    #rotates shape1_c.pos by cam because shape2_c.coord is also rotated by cam
    #this ensures all points are vel_y to date
    rotate([shape1_c.pos],pos,cam)
    #rotates shape2_c.coord opposite to the rotation of shape1
    #this allows the hitbox of shape1 to be found without having to rotate the hitbox
    rotate(shape2_c.coord,shape1_c.pos,[-shape1_c.ttheta[0],-shape1_c.ttheta[1],-shape1_c.ttheta[2]])
    #state is True if a point in shape2_c.coord is within hitbox of shape1_c
    state = False
    #hitbox equations are centered around point(0,0,0), so shape2_c.coord has to be moved opposite to shape1_c.pos
    for point in shape2_c.coord:
        point[0] -= shape1_c.pos[0]
        point[1] -= shape1_c.pos[1]
        point[2] -= shape1_c.pos[2]
        #determines if shape2 is in the hitbox of shape1 on xy plane, then the xz plane
        xy = abs(point[0]/(shape1_c.hitbox[0]/2)+point[1]/(shape1_c.hitbox[1]/2))+abs(point[0]/(shape1_c.hitbox[0]/2)-point[1]/(shape1_c.hitbox[1]/2)) <= 2
        xz = abs(point[0]/(shape1_c.hitbox[0]/2)+point[2]/(shape1_c.hitbox[2]/2))+abs(point[0]/(shape1_c.hitbox[0]/2)-point[2]/(shape1_c.hitbox[2]/2)) <= 2
        #if both are true, shape2 is in the hitbox of shape1
        if xy & xz:
            state = True
    return state

#creating and specifying objects
teapot = shapes("newell_teaset/teapot.obj")
#changes the velocity and cam angle of player
def move():
    keys_pressed = dict.fromkeys(['d','a','space','shift','w','s','right','left','up','down'],False)
    cam_at_press = dict.fromkeys(['d','a','space','shift','w','s','right','left','up','down'],0)
    cam_x = position.cam_x
    cam_y = position.cam_y
    def on_press(key):
        nonlocal cam_x
        nonlocal cam_y
        cam_x = position.cam_x
        cam_y = position.cam_y
        if key == pynput.keyboard.KeyCode.from_char('d') and keys_pressed['d'] == False:
            position.right(2,cam_y)
            keys_pressed['d'] = True
            cam_at_press['d'] = cam_y
        if key == pynput.keyboard.KeyCode.from_char('a') and keys_pressed['a'] == False:
            position.right(-2,cam_y)
            keys_pressed['a'] = True
            cam_at_press['a'] = cam_y
        if key == pynput.keyboard.Key.space and keys_pressed['space'] == False:
            position.up(2)
            keys_pressed['space'] = True
        if key == pynput.keyboard.Key.shift and keys_pressed['shift'] == False:
            position.up(-2)
            keys_pressed['shift'] = True
        if key == pynput.keyboard.KeyCode.from_char('w') and keys_pressed['w'] == False:
            position.forw(2,cam_x)
            keys_pressed['w'] = True
            cam_at_press['w'] = cam_x
        if key == pynput.keyboard.KeyCode.from_char('s') and keys_pressed['s'] == False:
            position.forw(-2,cam_x)
            keys_pressed['s'] = True
            cam_at_press['s'] = cam_x
        if key == pynput.keyboard.Key.right and keys_pressed['right'] == False:
            position.rt_y -= 0.1
            keys_pressed['right'] = True
        if key == pynput.keyboard.Key.left and keys_pressed['left'] == False:
            position.rt_y += 0.1
            keys_pressed['left'] = True
        if key == pynput.keyboard.Key.up and keys_pressed['up'] == False:
            position.rt_x -= 0.1
            keys_pressed['up'] = True
        if key == pynput.keyboard.Key.down and keys_pressed['down'] == False:
            position.rt_x += 0.1
            keys_pressed['down'] = True
        if key == pynput.keyboard.Key.esc:
            pygame.quit()
        if position.cam_y > (math.pi*2):
            position.cam_y -= (math.pi*2)
        if position.cam_y < 0:
            position.cam_y += (math.pi*2)
        if position.cam_x >= math.pi/2:
            position.cam_x = math.pi/2
        if position.cam_x <= -math.pi/2:
            position.cam_x = -math.pi/2
    def on_release(key):
        if key == pynput.keyboard.KeyCode.from_char('d'):
            position.right(-2,cam_at_press['d'])
            keys_pressed['d'] = False
        if key == pynput.keyboard.KeyCode.from_char('a'):
            position.right(2,cam_at_press['a'])
            keys_pressed['a'] = False
        if key == pynput.keyboard.Key.space:
            position.up(-2)
            keys_pressed['space'] = False
        if key == pynput.keyboard.Key.shift:
            position.up(2)
            keys_pressed['shift'] = False
        if key == pynput.keyboard.KeyCode.from_char('w'):
            position.forw(-2,cam_at_press['w'])
            keys_pressed['w'] = False
        if key == pynput.keyboard.KeyCode.from_char('s'):
            position.forw(2,cam_at_press['s'])
            keys_pressed['s'] = False
        if key == pynput.keyboard.Key.right:
            position.rt_y += 0.1
            keys_pressed['right'] = False
        if key == pynput.keyboard.Key.left:
            position.rt_y -= 0.1
            keys_pressed['left'] = False
        if key == pynput.keyboard.Key.up:
            position.rt_x += 0.1
            keys_pressed['up'] = False
        if key == pynput.keyboard.Key.down:
            position.rt_x -= 0.1
            keys_pressed['down'] = False
    def start_listener():
        with pynput.keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
            listener.join()
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()

def mouse_look():
    pygame.mouse.set_visible(False)
#    pygame.event.set_grab(True)
    mv = list(pygame.mouse.get_rel())
    cam[0] -= mv[1]*.01
    cam[1] += mv[0]*.01
    
#performs various tasks and calls functions
#all shape objects need to be passed into this function together so shapes are layered correctly
def exec_world(*shapes):
    #positions points.coord relative to points.pos
    for points in shapes:
        #rotates all shapes according to cam angle
        rotate(points.coord,pos,cam)
        #ttheta is the total rotation of a shape and is used to determine hitbox
        points.ttheta[0] = points.theta[0] + cam[0]
        points.ttheta[1] = points.theta[1] + cam[1]
        points.ttheta[2] = points.theta[2] + cam[2]
    #object "player" follows the cam and pos so the rotations and ttheta are reversed
    rotate(player.coord,pos,[-cam[0],0,0])
    rotate(player.coord,pos,[0,-cam[1],0])
    player.ttheta[0] = player.theta[0] - cam[0]
    player.ttheta[1] = player.theta[1] - cam[1]
    player.ttheta[2] = player.theta[2] - cam[2]
    draw_points(shapes)
   
create_SDL_window = drawPolygon.create_SDL_window
create_SDL_window.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
create_SDL_window.restypes = ctypes.c_void_p

create_SDL_renderer = drawPolygon.create_SDL_renderer
create_SDL_renderer.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint]
create_SDL_renderer.restypes = ctypes.c_void_p

draw_loop = drawPolygon.draw_polygon
draw_loop.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
draw_loop.restypes = None

window = create_SDL_window(b"Game Base", 0, 0, 1915, 1000, 0)
renderer = create_SDL_renderer(window, -1, 0)

def main():
    move()
    
    while True:
        start = time.time()
#        surface.fill(black)
        position.update()
        draw_points(teapot.points,teapot.shapes)
#        mouse_look()
#        position.pos[0]+=math.cos(position.cam[1])*position.vel_x
#        position.pos[2]-=math.sin(position.cam[1])*position.vel_x
#        pos[1]+=vel_y
#        pos[2]+=math.cos(cam[1])*vel_z
#        pos[0]+=math.sin(cam[1])*vel_z
        #draw text
#        pos_t = font.render('pos: '+str(int(pos[0]))+', '+str(int(pos[1]))+', '+str(int(pos[2])),True,red)
#        cam_t = font.render('cam: '+str(round(cam[0],1))+', '+str(round(cam[1],1))+', '+str(round(cam[2],1)),True,red)
#        surface.blit(pos_t,(0,0))
#        surface.blit(cam_t,(0,20))
#        pygame.display.update()
        end = time.time()
        if end-start < .017:
            time.sleep(.017-(end-start))

if __name__ == "__main__":
    main()
 
