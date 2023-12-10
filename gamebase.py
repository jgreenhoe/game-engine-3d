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
from pynput import keyboard
import threading
import queue
from handle_inputs import handle_inputs
screen = [1000,500]
#Declaring lists and variables
d = 500
#pos = [0,0,-10]
#vel_x = 0
#vel_y = 0
#vel_z = 0
#cam = [0,0,0]
#cam_vel_x = 0
#cam_vel_y = 0
drawPolygon = ctypes.PyDLL("/home/pi/Code/game-engine-3d/test.so")
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
        self.x += math.cos(cam_y)*a
        self.z -= math.sin(cam_y)*a
    def forw(self,a,cam_y):
        self.x += math.sin(cam_y)*a
        self.z += math.cos(cam_y)*a
    def up(self,a):
        self.y += a
position = position()
#turns objects of class shape into 2d points and draws it
def draw_points(points,faces):
#organize shapes by distance to pos
#shapes farthest away are drawn first
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
        
        shaped_points = shaped_points.astype(np.int32)
        shaped_points_ptr = shaped_points.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
        draw_loop(window,renderer,shaped_points.shape[0],shaped_points.shape[2],shaped_points_ptr)

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
def move(keys_pressed):
    keys_released = []
    speed = .5
    
    for i in range(0,handle_inputs.pressed_keys.qsize()):
        keys_pressed.append(handle_inputs.pressed_keys.get_nowait())
    for i in range(0,handle_inputs.released_keys.qsize()):
        keys_released.append(handle_inputs.released_keys.get_nowait())
    keys_pressed = list(set(keys_pressed)-set(keys_released))
    
    for i in keys_pressed:
        if (i) == 'd':
            position.right(speed,position.cam_y)
        if (i) == 'a':
            position.right(-speed,position.cam_y)
        if (i) == 's':
            position.forw(-speed,position.cam_y)
        if (i) == 'w':
            position.forw(speed,position.cam_y)
        if (i) == keyboard.Key.space:
            position.up(speed)
        if (i) == keyboard.Key.shift:
            position.up(-speed)
        
        if (i) == keyboard.Key.right:
            position.cam_y += 0.1
        if (i) == keyboard.Key.left:
            position.cam_y -= 0.1
        if (i) == keyboard.Key.up:
            position.cam_x += 0.1
        if (i) == keyboard.Key.down:
            position.cam_x -= 0.1
    
    return keys_pressed

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

window = create_SDL_window(b"Game Base", 0, 0, screen[0], screen[1], 0)
renderer = create_SDL_renderer(window, -1, 0)

handle_inputs = handle_inputs()
handle_inputs.start_thread()

def main():
    keys_pressed = []
    
    while True:
        start = time.time()
        keys_pressed = move(keys_pressed)
        position.update()
        draw_points(teapot.points,teapot.shapes)
        end = time.time()
        print(end-start)
        if end-start < .017:
            time.sleep(.017-(end-start))

if __name__ == "__main__":
    main()
 
