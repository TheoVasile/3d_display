import pygame as pg
from math import sqrt, atan, degrees, radians, sin, cos, tan, pi

pg.init()

#initialize display variables
w = 500
h = 500
screen = pg.display.set_mode((w,h))
pg.display.set_caption("3D")
clock = pg.time.Clock()

#euclidian distance of 2 dimensional points
def dist(pos1,pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

#midpoint of 3 dimensional points
def midpoint(point1, point2):
    x1, y1, z1 = point1[0], point1[1], point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    z = (z1 + z2) / 2

    return x,y,z

#average position among 3 dimensional points
def average(pos_list):
    average_pos = [0,0,0]
    for pos in pos_list:
        average_pos[0] += pos[0]
        average_pos[1] += pos[1]
        average_pos[2] += pos[2]
    average_pos = (average_pos[0]/len(average_pos),average_pos[1]/len(average_pos),average_pos[2]/len(average_pos))

    return average_pos

#determine the equation of the plane given 3 points
def find_plane_equation(point1,point2,point3):

    #define coordinates
    x1, y1, z1 = point1[0],point1[1],point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    x3, y3, z3 = point3[0], point3[1], point3[2]

    #find 2 vectors
    vector1 = (x1 - x2, y1 - y2, z1 - z2)
    vector2 = (x1 - x3, y1 - y3, z1 - z3)

    #find equation of normal
    a = (vector1[1] * vector2[2]) - (vector1[2] * vector2[1])
    b = (vector1[2] * vector2[0]) - (vector1[0] * vector2[2])
    c = (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])

    #find displacement
    d = -((x1 * a) + (y1 * b) + (z1 * c))

    return d, a, b, c

def pivot(pivot_point, coordinate, x_rot, y_rot, z_rot):
    rotations = [x_rot, y_rot, z_rot]

    for axis_index in range(0,3):
        distance = dist((coordinate[axis_index - 2], coordinate[axis_index - 1]), (pivot_point[axis_index - 2], pivot_point[axis_index - 1]))
        angle = 0
        rise = coordinate[axis_index - 2] - pivot_point[axis_index - 2]
        run = coordinate[axis_index - 1] - pivot_point[axis_index - 1]
        try:
            slope = rise / run
            angle = degrees(atan(slope))
        except:
            if rise > 0:
                angle = 90
            elif rise < 0:
                angle = -90

        if run < 0:
            angle += 180

        angle += rotations[axis_index]
        print (coordinate[axis_index - 2])
        print (distance * sin(radians(angle)))
        coordinate[axis_index - 2] = distance * sin(radians(angle))
        coordinate[axis_index - 1] = distance * cos(radians(angle))

    return coordinate

def move_to_target(xe,ye,target_pos, displace):
    #initialize variables
    target_x = target_pos[0]
    target_y = target_pos[1]

    #calculate the angle needed to move to the desired position
    risee = target_y - ye
    rune = target_x - xe

    anglee = 0

    #account for angle irregularities
    try:
        slope = risee/rune
        anglee = degrees(atan(slope))
    except:
        if risee > 0:
            anglee = 90
        elif risee < 0:
            anglee = -90
        elif risee == 0:
            anglee = 0
    if rune < 0:
        anglee += 180
    while anglee < 0:
        anglee += 360
    while anglee > 360:
        anglee -= 360

    return anglee

class vertice:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.screen_pos = [0,0] #position of point on the screen
        self.vertice_selected = False
    def get_pos(self):
        return self.x,self.y,self.z
    def get_screen_pos(self):
        return self.screen_pos
    def set_pos(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def set_screen_pos(self,x,y):
        self.screen_pos = [x,y]
    def selected(self):
        return self.vertice_selected
    def set_selected(self, value):
        self.vertice_selected = value

#display object
class camera:
    def __init__(self,x, y, z, scale, focal_length):
        self.x = x
        self.y = y
        self.z = z
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.pivot_point = [self.x, self.y, self.z]
        self.focal_length = focal_length
        #self.d, self.a, self.b, self.c = list(find_plane_equation(self.x_edges[0][0],self.x_edges[0][1], self.x_edges[1][0]))
        #self.plane_equation = [self.d, self.a, self.b, self.c]

    def draw_edge(self,edge,perspective):
        self.positions = []
        for self.vertex in edge:
            self.vertex_pos = list(self.vertex.get_pos())
            print (self.vertex_pos)
            self.vertex_pos = pivot([self.x, self.y, self.z], self.vertex_pos, -self.angle_x, -self.angle_y, -self.angle_z)
            self.vertex_x = self.vertex_pos[0]
            self.vertex_y = self.vertex_pos[1]
            self.vertex_z = self.vertex_pos[2]
            if perspective:
                #find y coordinate on screen
                self.rise = self.vertex_z - self.z
                self.run = self.vertex_y - self.y
                try:
                    self.slope = self.rise / self.run
                    self.b = self.z - self.slope * self.y
                    self.screen_y = self.slope * (self.x + self.focal_length) + self.b

                except:
                    self.screen_y = self.y

                #find x coordinates on screen
                self.rise = self.vertex_y - self.y
                self.run = self.vertex_x - self.x
                try:
                    self.slope = self.rise / self.run
                    if self.slope == 0:
                        self.screen_x = self.x
                    else:
                        self.b = self.y - self.slope * self.x
                        self.screen_x = ((self.z + self.focal_length) - self.b) / self.slope
                except:
                    self.screen_x = self.x

                self.vertex.set_screen_pos(self.screen_x + (w/2), self.screen_y + (h/2))
                self.positions.append((self.screen_x + (w/2), self.screen_y + (h/2)))
                self.screen_point = [self.screen_x + (w/2), self.y, self.screen_y + (h/2)]

            elif not perspective:
                self.vertex.set_screen_pos(self.vertex_x + (w/2), self.vertex_z + (h/2))
                self.positions.append((self.vertex_x + (w/2), self.vertex_z + (h/2)))
                self.screen_point = [self.vertex_x + (w / 2), self.vertex_y, self.vertex_z + (h / 2)]

            #draw vertices only in edit_mode
            if edit_mode:
                if self.vertex.selected() and edit_mode:
                    pg.draw.circle(screen,(0,200,255),(int(self.screen_point[0]), int(self.screen_point[2])),2,0)
                else:
                    pg.draw.circle(screen,(255,255,255),(int(self.screen_point[0]), int(self.screen_point[2])),2,0)
                pg.draw.circle(screen, (255, 0, 0),(int(self.vertex.get_pos()[1] + 100), int(self.vertex.get_pos()[2] + 100)), 2, 0)
                pg.draw.circle(screen, (0, 255, 0),(int(self.vertex.get_pos()[0] + 400), int(self.vertex.get_pos()[2] + 100)), 2, 0)
                pg.draw.circle(screen, (0, 0, 255),(int(self.vertex.get_pos()[0] + 400), int(self.vertex.get_pos()[1] + 300)), 2, 0)

        pg.draw.line(screen,(100,100,100), self.positions[0], self.positions[1],1)
        pg.draw.line(screen, (255, 0, 0), (edge[0].get_pos()[1] + 100, edge[0].get_pos()[2] + 100),(edge[1].get_pos()[1] + 100, edge[1].get_pos()[2] + 100), 1)
        pg.draw.line(screen, (0, 255, 0), (edge[0].get_pos()[0] + 400, edge[0].get_pos()[2] + 100),(edge[1].get_pos()[0] + 400, edge[1].get_pos()[2] + 100), 1)
        pg.draw.line(screen, (0, 0, 255), (edge[0].get_pos()[0] + 400, edge[0].get_pos()[1] + 300),(edge[1].get_pos()[0] + 400, edge[1].get_pos()[1] + 300), 1)

    def rotate(self,x_rot,y_rot,z_rot):
        self.angle_x += x_rot
        self.angle_y += y_rot
        self.angle_z += z_rot

    def translate(self, displace):
        self.x += displace * sin(radians(self.angle_z))
        self.y += displace * cos(radians(self.angle_z))
        self.z += displace * sin(radians(self.angle_x))

    def display(self,objects, perspective):
        for self.object in objects:
            for self.edge in self.object.get_edges():
                self.draw_edge(self.edge, perspective)

class sphere:
    def __init__(self,x,y,z,scale,segments,rings):
        self.vertices = []
        self.ring_angle_increment = 180 / rings
        self.segment_angle_increment = 360 / segments
        self.anglez = self.ring_angle_increment / 2
        self.angley = 0
        self.z = (30 * scale) + z
        self.y = y
        self.x = x
        self.displacement = (2 * pi * dist((0,self.z),(0,z))) / rings
        self.edges = []
        self.points = []
        self.pivot_point = (x, y, z)
        for y in range(0,rings):
            self.anglez -= self.ring_angle_increment
            self.z += self.displacement * sin(radians(self.anglez))
            self.x += self.displacement * cos(radians(self.anglez))
            self.rad = dist((0, 0), (self.x, self.y))
            for x in range(0,segments):
                self.angley -= self.segment_angle_increment
                self.disp = (2 * self.rad * pi) / segments
                self.y += self.disp * cos(radians(self.angley))
                self.x += self.disp * sin(radians(self.angley))
                self.vertices.append(vertice(self.x,self.y,self.z))
                self.points.append((self.x,self.y,self.z))
                try:
                    self.edges.append([self.vertices[-1],self.vertices[-2]])
                except:
                    pass

    def rotate(self,velocity):
        #rotate around each axis
        for index in range(0,3):
            self.axis = [velocity[0],velocity[1],velocity[2]][index]

            print ("wow = {}".format(self.vertices))

            #rotate every vertex around the pivot point
            for self.vertex in self.vertices:
                self.pos = list(self.vertex.get_pos())
                self.distance = dist((self.vertex.get_pos()[index-2], self.vertex.get_pos()[index-1]),(self.pivot_point[index-2],self.pivot_point[index-1]))
                self.rise = self.pos[index-2] - self.pivot_point[index-2]
                self.run = self.pos[index-1] - self.pivot_point[index-1]

                #account for angle irregularities
                try:
                    self.slope = self.rise/self.run
                    self.angle = degrees(atan(self.slope))
                except:
                    if self.rise > 0:
                        self.angle = 90
                    elif self.rise < 0:
                        self.angle = -90
                    elif self.rise == 0:
                        self.angle = 0
                if self.run < 0:
                    self.angle += 180

                self.angle += self.axis

                #update of vertex
                self.pos[index-2] = self.distance * sin(radians(self.angle))
                self.pos[index-1] = self.distance * cos(radians(self.angle))

                self.x = self.pos[0]
                self.y = self.pos[1]
                self.z = self.pos[2]

                self.vertex.set_pos(self.x, self.y, self.z)

    def get_edges(self):
        return self.edges

class cube:
    def __init__(self,scale):
        #initialize variables
        self.vertices = []
        self.edges = []
        self.pivot_point = [0,0,0]
        self.positions = []

        #set vertices of cube
        for x in [-scale,scale]:
            for y in [-scale,scale]:
                for z in [-scale,scale]:
                    self.vertices.append(vertice(x,y,z))
                    self.pivot_point[0] += x
                    self.pivot_point[1] += y
                    self.pivot_point[2] += z
                    self.positions.append((x,y,z))

        #set edges of cube
        self.edges.append((self.vertices[0], self.vertices[1]))
        self.edges.append((self.vertices[0], self.vertices[2]))
        self.edges.append((self.vertices[0], self.vertices[4]))
        self.edges.append((self.vertices[3], self.vertices[1]))
        self.edges.append((self.vertices[3], self.vertices[2]))
        self.edges.append((self.vertices[3], self.vertices[7]))
        self.edges.append((self.vertices[6], self.vertices[4]))
        self.edges.append((self.vertices[6], self.vertices[7]))
        self.edges.append((self.vertices[6], self.vertices[2]))
        self.edges.append((self.vertices[5], self.vertices[1]))
        self.edges.append((self.vertices[5], self.vertices[7]))
        self.edges.append((self.vertices[5], self.vertices[4]))

        #self.faces = []
        #self.faces.append((self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]))
        #self.faces.append((self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]))
        #self.faces.append((self.vertices[0], self.vertices[2], self.vertices[4], self.vertices[6]))
        #self.faces.append((self.vertices[2], self.vertices[3], self.vertices[5], self.vertices[8]))
        #self.faces.append((self.vertices[5], self.vertices[4], self.vertices[6], self.vertices[7]))
        #self.faces.append((self.vertices[2], self.vertices[3], self.vertices[6], self.vertices[7]))

        self.pivot_point = average(self.positions)

        self.selected_vertices = []

    def rotate(self,velocity):
        #rotate around each axis
        for index in range(0,3):
            self.axis = [velocity[0],velocity[1],velocity[2]][index]


            #rotate every vertex around the pivot point
            for self.vertex in self.vertices:
                self.pos = list(self.vertex.get_pos())
                self.distance = dist((self.vertex.get_pos()[index-2], self.vertex.get_pos()[index-1]),(self.pivot_point[index-2],self.pivot_point[index-1]))
                self.rise = self.pos[index-2] - self.pivot_point[index-2]
                self.run = self.pos[index-1] - self.pivot_point[index-1]

                #account for angle irregularities
                try:
                    self.slope = self.rise/self.run
                    self.angle = degrees(atan(self.slope))
                except:
                    if self.rise > 0:
                        self.angle = 90
                    elif self.rise < 0:
                        self.angle = -90
                    elif self.rise == 0:
                        self.angle = 0
                if self.run < 0:
                    self.angle += 180

                self.angle += self.axis

                #update pos of vertex
                self.pos[index-2] = self.distance * sin(radians(self.angle))
                self.pos[index-1] = self.distance * cos(radians(self.angle))

                self.x = self.pos[0]
                self.y = self.pos[1]
                self.z = self.pos[2]

                self.vertex.set_pos(self.x, self.y, self.z)

    def select_vert(self,mouse_pos):
        self.search_radius = 5
        for self.vertex in self.vertices:
            if keys[pg.K_a]:
                print ("select all")
                if len(self.selected_vertices) < 1:
                    self.selected_vertices.append(self.vertex)
                    self.vertex.set_selected(True)
                elif len(self.selected_vertices) > 0:
                    try:
                        self.selected_vertices.remove(self.vertex)
                        self.vertex.set_selected(False)
                    except:
                        pass
            elif not keys[pg.K_LSHIFT]:
                try:
                    self.selected_vertices.remove(self.vertex)
                    self.vertex.set_selected(False)
                except:
                    if dist(mouse_pos, self.vertex.get_screen_pos()) < self.search_radius:
                        print ("yate")
                        try:
                            self.selected_vertices.remove(self.vertex)
                            self.vertex.set_selected(False)
                        except:
                            self.selected_vertices.append(self.vertex)
                            self.vertex.set_selected(True)
            elif keys[pg.K_LSHIFT]:
                if dist(mouse_pos, self.vertex.get_screen_pos()) < self.search_radius:
                    print("yate")
                    try:
                        self.selected_vertices.remove(self.vertex)
                        self.vertex.set_selected(False)
                    except:
                        self.selected_vertices.append(self.vertex)
                        self.vertex.set_selected(True)
    def edit(self):
        for self.vertex in self.selected_vertices:
            self.vert_x, self.vert_y, self.vert_z = self.vertex.get_pos()
            self.vert_x += vx
            self.vert_z += vy
            self.vertex.set_pos(self.vert_x, self.vert_y, self.vert_z)

    def get_edges(self):
        return self.edges

    def display(self):
        for self.edge in self.edges:
            cam.draw_edge(self.edge,True)

cam = camera(0, 100, 0, 1, 1) #define camera
object = cube(50) #make a cube object
#object = sphere(0,0,0,1,16,8)
previous_mouse_pos = [0, 0]
current_mouse_pos = [0, 0]
objects = [object] #stores every object in a scene
move_vert = False

edit_mode = False

running = True

perspective = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_KP5:
                perspective = [True,False][[True, False].index(perspective) - 1]
            if event.key == pg.K_TAB:
                edit_mode = [True,False][[True,False].index(edit_mode) - 1]
                print ("edit mode = {}".format(edit_mode))
            if event.key == pg.K_g and edit_mode:
                move_vert = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                cam.translate(-5)
            elif event.button == 5:
                cam.translate(5)
            print ("yeee")
            if edit_mode:
                move_vert = False
                if pg.mouse.get_pressed()[2]:
                    object.select_vert(pg.mouse.get_pos())
                    print("edit object")
    current_mouse_pos = pg.mouse.get_pos()
    #draw elements to the screen
    screen.fill((0,0,0))

    vx, vy = current_mouse_pos[0] - previous_mouse_pos[0], current_mouse_pos[1] - previous_mouse_pos[1]

    if pg.mouse.get_pressed()[1]:
        #object.rotate((vy,0,-vx))
        cam.rotate(vy,0,vx)
        #object.rotate((3, 1, 2))

    keys = pg.key.get_pressed()
    if move_vert:
        if edit_mode:
            print("edit")
            object.edit()
        else:
            move_vert = False
    if keys[pg.K_KP4]:
        cam.rotate(0, 0, 2.5)
    elif keys[pg.K_KP6]:
        cam.rotate(0, 0, -2.5)
    elif keys[pg.K_KP8]:
        cam.rotate(2.5, 0, 0)
    elif keys[pg.K_KP2]:
        cam.rotate(-2.5, 0, 0)

    #cam.rotate(0,0,1)
    cam.display(objects, perspective) #display all the objects to the screen
    previous_mouse_pos = current_mouse_pos

    #update screen
    pg.display.update()
    clock.tick(60)