import pygame as pg
from math import sqrt, atan, degrees, radians, sin, cos, tan, pi

pg.init()

w = 500
h = 500
screen = pg.display.set_mode((w,h))
pg.display.set_caption("3D")
clock = pg.time.Clock()

def dist(pos1,pos2):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def midpoint(point1, point2):
    x1, y1, z1 = point1[0], point1[1], point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2
    z = (z1 + z2) / 2

    return x,y,z

def average(pos_list):
    average_pos = [0,0,0]
    for pos in pos_list:
        average_pos[0] += pos[0]
        average_pos[1] += pos[1]
        average_pos[2] += pos[2]
    average_pos = (average_pos[0]/len(average_pos),average_pos[1]/len(average_pos),average_pos[2]/len(average_pos))

    return average_pos

def find_plane_equation(point1,point2,point3):

    x1, y1, z1 = point1[0],point1[1],point1[2]
    x2, y2, z2 = point2[0], point2[1], point2[2]
    x3, y3, z3 = point3[0], point3[1], point3[2]

    x,y,z = 0,0,0

    vector1 = (x1 - x2, y1 - y2, z1 - z2)
    vector2 = (x1 - x3, y1 - y3, z1 - z3)

    a = (vector1[1] * vector2[2]) - (vector1[2] * vector2[1])
    b = (vector1[2] * vector2[0]) - (vector1[0] * vector2[2])
    c = (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])

    d = -((x1 * a) + (y1 * b) + (z1 * c))

    return d, a, b, c

class camera:
    def __init__(self,x,y,z,scale):
        self.x = x
        self.y = y
        self.z = z
        self.slope = 0
        self.displace = 100 * scale
        self.pivot_point = [self.x, self.y, self.z]

        self.x_edges = [[[self.x + self.displace,self.y,self.z + self.displace],[self.x + self.displace,self.y,self.z - self.displace]],[[self.x - self.displace,self.y,self.z + self.displace],[self.x - self.displace,self.y,self.z - self.displace]]]
        self.y_edges = [[[self.x + self.displace, self.y, self.z + self.displace], [self.x - self.displace, self.y, self.z + self.displace]],[[self.x + self.displace, self.y, self.z - self.displace], [self.x - self.displace, self.y, self.z - self.displace]]]
        self.edges = [self.x_edges,self.y_edges]

        self.d, self.a, self.b, self.c = find_plane_equation(self.x_edges[0][0],self.x_edges[0][1], self.x_edges[1][0])
        self.plane_equation = [self.d, self.a, self.b, self.c]

    def draw_edge(self,edge):
        self.positions = []
        for self.vertex in edge:
            self.vertex_pos = self.vertex.get_pos()
            self.vertex_x = self.vertex_pos[0] - self.a
            self.vertex_y = self.vertex_pos[1] - self.b
            self.vertex_z = self.vertex_pos[2] - self.c

            self.t = self.vertex_x + self.vertex_y + self.vertex_z
            self.t = self.d / self.t
            self.dist = dist((self.vertex_pos[0] + self.t * self.a, self.vertex_pos[1] + self.t * self.b, (self.vertex_pos[2] + self.t * self.c)), self.vertex_pos)
            self.screen_point = [(self.vertex_pos[0] + self.t * self.a) + (w/2) + self.x, self.vertex_pos[1] + self.t * self.b + self.y, (self.vertex_pos[2] + self.t * self.c) + (h/2) + self.z]
            print (self.screen_point)
            #self.screen_point[0] = self.screen_point[0] + (sqrt(sqrt(self.dist)) * (((w / 2) - self.screen_point[0]) / abs((w / 2) - self.screen_point[0])))
            #self.screen_point[2] = self.screen_point[2] + (sqrt(sqrt(self.dist)) * (((h / 2) - self.screen_point[2]) / abs((h / 2) - self.screen_point[2])))
            self.positions.append((self.screen_point[0],self.screen_point[2]))
            print(self.screen_point)
            print (sqrt(sqrt(self.dist)))
            print ("--------------------")

            pg.draw.circle(screen,(255,255,255),(int(self.screen_point[0]),int(self.screen_point[2])),2,0)
            pg.draw.circle(screen, (255, 0, 0),(int(self.vertex.get_pos()[1] + 100), int(self.vertex.get_pos()[2] + 100)), 2, 0)
            pg.draw.circle(screen, (0, 255, 0),(int(self.vertex.get_pos()[0] + 400), int(self.vertex.get_pos()[2] + 100)), 2, 0)
            pg.draw.circle(screen, (0, 0, 255),(int(self.vertex.get_pos()[0] + 400), int(self.vertex.get_pos()[1] + 300)), 2, 0)

        pg.draw.line(screen,(100,100,100),self.positions[0],self.positions[1],1)

    def rotate(self,x_rot,y_rot,z_rot):
        for self.axis_index in range(0,3):
            self.axis = [x_rot,y_rot,z_rot][self.axis_index]
            for self.edge_axis_index in range(0,len(self.edges)):
                for self.edge_index in range(0,2):
                    for self.pos_index in range(0,2):
                        self.pos = self.edges[self.edge_axis_index][self.edge_index][self.pos_index]
                        print ("pos = {}".format(self.pos))
                        self.distance = dist((self.pos[self.axis_index - 2], self.pos[self.axis_index - 1]), (self.pivot_point[self.axis_index - 2], self.pivot_point[self.axis_index - 1]))
                        print ("dist = {}")
                        self.rise = self.pos[self.axis_index - 2] - self.pivot_point[self.axis_index - 2]
                        self.run  = self.pos[self.axis_index - 1] - self.pivot_point[self.axis_index - 1]

                        # account for angle irregularities
                        try:
                            self.slope = self.rise / self.run
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

                        # update of vertex
                        self.pos[self.axis_index - 2] = self.distance * sin(radians(self.angle))
                        self.pos[self.axis_index - 1] = self.distance * cos(radians(self.angle))

                        #self.x = self.pos[0]
                        #self.y = self.pos[1]
                        #self.z = self.pos[2]

                        self.edges[self.edge_axis_index][self.edge_index][self.pos_index] = self.pos
        self.d, self.a, self.b, self.c = find_plane_equation(self.x_edges[0][0], self.x_edges[0][1], self.x_edges[1][0])

    def display(self,objects):
        for self.object in objects:
            for self.edge in self.object.get_edges():
                self.draw_edge(self.edge)

class sphere:
    def __init__(self,scale,segments,rings):
        self.vertices = []
        self.ring_angle_increment = 180 / rings
        self.segment_angle_increment = 360 / segments
        self.anglez = self.ring_angle_increment / 2
        self.angley = 0
        self.z = 100 * scale
        self.y = 0
        self.x = 0
        self.displacement = 10 * scale
        self.edges = []
        self.points = []
        for y in range(1,rings):
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
        self.pivot_point = average(self.points)

    def rotate(self,velocity):
        #rotate around each axis
        for index in range(0,3):
            self.axis = [velocity[0],velocity[1],velocity[2]][index]

            print ("wow = {}".format(self.vertices))

            #rotate every vertex around the pivot point
            for self.vertex in self.vertices:
                self.pos = list(self.vertex.get_pos())
                self.distance = dist((self.vertex.get_pos()[index-2], self.vertex.get_pos()[index-1]),(0,0))
                self.rise = self.pos[index-2]# - self.pivot_point[index-2]
                self.run = self.pos[index-1]# - self.pivot_point[index-1]

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

class vertice:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.distance = 0
    def get_pos(self):
        return self.x,self.y,self.z
    def set_pos(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

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

        self.pivot_point = average(self.positions)

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

    def get_edges(self):
        return self.edges

    def display(self):
        for self.edge in self.edges:
            cam.draw_edge(self.edge)

cam = camera(0, 100, 0, 1) #define camera
object = cube(50) #make a cube object
object = sphere(1,32,16)
previous_mouse_pos = [0, 0]
current_mouse_pos = [0, 0]
objects = [object] #stores every object in a scene

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    current_mouse_pos = pg.mouse.get_pos()

    #draw elements to the screen
    screen.fill((0,0,0))

    if pg.mouse.get_pressed()[0] or True:
        vx,vy = current_mouse_pos[0] - previous_mouse_pos[0], current_mouse_pos[1] - previous_mouse_pos[1]
        object.rotate((1,1,0))

    #cam.rotate(0,0,1)
    cam.display(objects) #display all the objects to the screen
    previous_mouse_pos = current_mouse_pos

    #update screen
    pg.display.update()
    clock.tick(60)