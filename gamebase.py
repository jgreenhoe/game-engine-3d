#import libraries
import math
import random
import numpy as np
import time
import ctypes.util
from pynput import keyboard
import threading
import queue
from handle_inputs import handle_inputs
#Declaring lists and variables
screen = [1000,500]
d = 500
#.so file compiled from draw_loop.c
drawPolygon = ctypes.PyDLL("/home/pi/Code/game-engine-3d/drawPolygons.so")

#class of organized data extracted from .obj file
class read_obj:
    def __init__(self, obj_file):
        self.v = []
        self.vt = []
        self.vn = []
        self.fv = []
        self.fvt = []
        self.fvn = []
        with open(obj_file) as file:
            for line in file:
                if line[:2] == "v ":
                    x = line.find(" ") + 1
                    y = line.find(" ",x) + 1
                    z = line.find(" ",y) + 1
                    self.v.append([float(line[x:y]),float(line[y:z]),float(line[z:-1])])
                elif line[:2] == "vt":
                    x = line.find(" ") + 1
                    y = line.find(" ",x) + 1
                    self.vt.append([float(line[x:y]),float(line[y:-1])])
                elif line[:2] == "vn":
                    x = line.find(" ") + 1
                    y = line.find(" ",x) + 1
                    z = line.find(" ",y) + 1
                    self.vn.append([float(line[x:y]),float(line[y:z]),float(line[z:-1])])
                elif line[0] == 'f':
                    if line[-1] != " ":
                        line += " "
                    f_v = []
                    f_vt = []
                    f_vn = []
                    start_pos = 1
                    start_type = " "
                    counter = 2
                    for char in line[2:]:
                        if char == " ":
                            if start_type == " " and line[start_pos+1:counter] != '\n':
                                f_v.append(int(line[start_pos+1:counter]))
                            if start_type == "/":
                                f_vn.append(int(line[start_pos+1:counter]))
                            start_pos = counter
                            start_type = " "
                        elif char == "/":
                            if start_type == " ":
                                f_v.append(int(line[start_pos+1:counter]))
                            if start_type == "/" and start_pos+1 != counter:
                                f_vt.append(int(line[start_pos+1:counter]))
                            start_pos = counter
                            start_type = "/"
                        counter += 1
                    self.fv.append(f_v)
                    self.fvt.append(f_vt)
                    self.fvn.append(f_vn)
                    
class read_mtl:
    def __init__(self,mtl_file):
        with open(obj_file) as file:
            for line in file:
                if line[:6] == "newmtl":
                    pass

#class of the camera position and rotation
class position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = -10
        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = 0
        self.pos = [self.x, self.y, self.z]
        self.cam = [self.cam_x, self.cam_y, self.cam_z]
    def update(self):
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

class objects(position):
    def __init__(self,obj_file):
        obj = read_obj(obj_file)
        self.points = np.array(obj.v)
        self.normals = np.array(obj.vn)
        #find the maximum amount of vertex indexes a face has
        max_len = len(max(obj.fv, key=len))
        #increase the number of vertex indexes in each face until 
        #each face has max_len vertex indexes
        #this allows the face array to be converted to np.array
        for i in obj.fv:
            while len(i) < max_len:
                i.append(i[-1])
        #repeate the process of vertex faces for vertex normal faces
        max_len = len(max(obj.fvn, key=len))
        for i in obj.fvn:
            while len(i) < max_len:
                i.append(i[-1])
        #convert vertex and vertex normal faces to np.array
        self.vfaces = np.array(obj.fv)
        self.nvfaces = np.array(obj.fvn)
        max_color = 2200
        self.colors = np.array([np.linspace(0,75,max_color),np.full(max_color, 100),np.full(max_color, 100)])
        
        self.hitbox = self.Hitbox(self)
        
        super().__init__()
        self.points[:,0] += self.x
        self.points[:,1] += self.y
        self.points[:,2] += self.z
        self.orig_points = self.points
        
    def update(self):
        self.pos = [self.x, self.y, self.z]
        self.cam = [self.cam_x, self.cam_y, self.cam_z]
        self.points = self.orig_points + self.pos
        
        
    class Hitbox:
        def __init__(self, objects):
            vert_dist = np.linalg.norm(objects.points[0])
            xbound = [objects.points[0][0], objects.points[0][0]]
            ybound = [objects.points[0][1], objects.points[0][1]]
            zbound = [objects.points[0][2], objects.points[0][2]]
            self.sphere_bound_index = 0
            self.xbound_index = [0, 0]
            self.ybound_index = [0, 0]
            self.zbound_index = [0, 0]
            index_counter = 0
            for i in objects.points:
                if np.linalg.norm(i) > vert_dist:
                    vert_dist = np.linalg.norm(i)
                    self.sphere_bound_index = index_counter
                    
                if i[0] < xbound[0]:
                    xbound[0] = i[0]
                    self.xbound_index[0] = index_counter
                elif i[0] > xbound[1]:
                    xbound[1] = i[0]
                    self.xbound_index[1] = index_counter
                if i[1] < ybound[0]:
                    ybound[0] = i[1]
                    self.ybound_index[0] = index_counter
                elif i[1] > ybound[1]:
                    ybound[1] = i[1]
                    self.ybound_index[1] = index_counter
                if i[2] < zbound[0]:
                    zbound[0] = i[2]
                    self.zbound_index[0] = index_counter
                elif i[2] > zbound[1]:
                    zbound[1] = i[2]
                    self.zbound_index[1] = index_counter
                index_counter += 1

                
    #multiplies self.shape by size multiplier
    def set_size(self,size):
        #size format: [x, y, z]
        for i in self.points:
            i[0] = i[0]*size[0]
            i[1] = i[1]*size[1]
            i[2] = i[2]*size[2]

#create instance of position for player position
cam_position = position()
#calculates optimized 2d coordinates from 'shapes' instances,
#then calls the draw_loop function from drawPolygon to render
def draw_points(obj):
    points = obj.points
    normals = obj.normals
    faces = obj.vfaces
    nvfaces = obj.nvfaces
    colors = obj.colors
    
    rotated_points = rotate(points,cam_position.pos,cam_position.cam)
    rotated_normals = rotate(normals, [0,0,0],cam_position.cam)
    #rotated_points format: [[x, y, z], [x, y, z]...]

    #filter in only the faces that contain vertices whose normals face the camera
    bool_normals_drawn = rotated_normals[:,2] < 0
    bool_polygon_normals = bool_normals_drawn[nvfaces-1]
    bool_vertices_drawn = np.any(bool_polygon_normals,1)
    faces = faces[bool_vertices_drawn]
    
    #filter in only the faces in front of the camera
    bool_vertices_drawn = rotated_points[:,2] > cam_position.z
    bool_polygons_drawn = bool_vertices_drawn[faces-1]
    bool_faces_drawn = np.any(bool_polygons_drawn,1)
    faces = faces[bool_faces_drawn]
    
    #compute array of 2d coordinates from rotated_points
    flat = np.array((d*(rotated_points[:,0]-cam_position.pos[0])/(rotated_points[:,2]-cam_position.pos[2])+screen[0]/2,-d*(rotated_points[:,1]-cam_position.pos[1])/(rotated_points[:,2]-cam_position.pos[2])+screen[1]/2))
    #flat format: [[x, x...], [y, y...]]

    #reformat arrays to pass into draw_loop
    flat = np.swapaxes(flat,0,1)
    #flat format: [[x, y], [x, y]...]
    
    faces_array = np.array(faces)
    shaped_points = flat[faces_array-1]
    #shaped_points format: [[[x, y], [x, y]...]...]
    
    #organize polygons by distance to camera position
    #shapes farthest away are drawn first
    sort_points = np.linalg.norm(rotated_points[faces_array[:,0]-1]-cam_position.pos,axis=1)
    sort_index = np.argsort(sort_points)
    shaped_points = shaped_points[np.flip(sort_index)]
    shaped_points = np.ascontiguousarray(np.swapaxes(shaped_points,1,2))
    
    #configure color data
    colors = np.swapaxes(colors,0,1)
    colors = colors[np.flip(sort_index)]

    #prepare pointer of shaped_points compatible with draw_loop
    shaped_points = shaped_points.astype(np.float32)
    shaped_points_ptr = shaped_points.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    colors = colors.astype(np.float32)
    colors_ptr = colors.ctypes.data_as(ctypes.POINTER(ctypes.c_float))
    draw_loop(window,renderer,shaped_points.shape[0],shaped_points.shape[2],shaped_points_ptr, colors_ptr)

#rotates shape around points by theta
#shape format [[x,y,z],[x,y,z]...] point format [x,y,z] theta format [x,y,z]
def rotate(shape,point,theta):
    sc = np.copy(shape)
    #rotate around y-axis
    cos = np.cos(theta[1])
    sin = np.sin(theta[1])
    x = sc[:,0]-point[0]
    z = sc[:,2]-point[2]
    sc[:,0] = x*cos-z*sin+point[0]
    sc[:,2] = z*cos+x*sin+point[2]
    
    #rotate around x-axis
    cos = np.cos(theta[0])
    sin = np.sin(theta[0])
    y = sc[:,1]-point[1]
    z = sc[:,2]-point[2]
    sc[:,1] = y*cos-z*sin+point[1]
    sc[:,2] = z*cos+y*sin+point[2]
    
    #rotate around z-axis
    cos = np.cos(theta[2])
    sin = np.sin(theta[2])
    x = sc[:,0]-point[0]
    y = sc[:,1]-point[1]
    sc[:,0] = x*cos-y*sin+point[0]
    sc[:,1] = y*cos+x*sin+point[1]
    
    return sc

#creating and specifying objects
teapot = objects("newell_teaset/teapot.obj")
player = objects("/home/pi/Downloads/sphere.obj")
#teapot = objects("/home/pi/Downloads/Gun.obj")
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
            cam_position.right(speed,cam_position.cam_y)
        if (i) == 'a':
            cam_position.right(-speed,cam_position.cam_y)
        if (i) == 's':
            cam_position.forw(-speed,cam_position.cam_y)
        if (i) == 'w':
            cam_position.forw(speed,cam_position.cam_y)
        if (i) == keyboard.Key.space:
            cam_position.up(speed)
        if (i) == keyboard.Key.shift:
            cam_position.up(-speed)
        
        if (i) == keyboard.Key.right:
            cam_position.cam_y += 0.1
        if (i) == keyboard.Key.left:
            cam_position.cam_y -= 0.1
        if (i) == keyboard.Key.up:
            cam_position.cam_x += 0.1
        if (i) == keyboard.Key.down:
            cam_position.cam_x -= 0.1
            
        if cam_position.cam_x >= 1.57:
            cam_position.cam_x = 1.57
        if cam_position.cam_x <= -1.57:
            cam_position.cam_x = -1.57
        if cam_position.cam_y > 6.24:
            cam_position.cam_y = 0
        if cam_position.cam_y < -6.24:
            cam_position.cam_y = 0
    
    return keys_pressed
   
def detect_hitbox(obj1, obj2):
    dist = np.linalg.norm(obj1.points[obj1.hitbox.sphere_bound_index]-obj2.points[obj2.hitbox.sphere_bound_index])
    print(dist)

create_SDL_window = drawPolygon.create_SDL_window
create_SDL_window.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
create_SDL_window.restypes = ctypes.c_void_p

create_SDL_renderer = drawPolygon.create_SDL_renderer
create_SDL_renderer.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_uint]
create_SDL_renderer.restypes = ctypes.c_void_p

clear_SDL_renderer = drawPolygon.clear_SDL_renderer
clear_SDL_renderer.argtypes = [ctypes.c_void_p]
clear_SDL_renderer.restypes = None

present_SDL_renderer = drawPolygon.present_SDL_renderer
present_SDL_renderer.argtypes = [ctypes.c_void_p]
present_SDL_renderer.restypes = None

draw_loop = drawPolygon.draw_polygon
draw_loop.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int,ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)]
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
        cam_position.update()
        player.x = cam_position.x
        player.y = cam_position.y - 20
        player.z = cam_position.z + 70
        player.update()
        detect_hitbox(teapot, player)
        clear_SDL_renderer(renderer)
        draw_points(teapot)
        draw_points(player)
        present_SDL_renderer(renderer)
        end = time.time()
        #control framerate
        if end-start < .017:
            time.sleep(.017-(end-start))
        #print(end-start)

if __name__ == "__main__":
    main()
