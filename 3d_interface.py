import pygame as pg
from math import sqrt, atan, degrees, radians, sin, cos, tan

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

    #print ("{} = {}x + {}y + {}z".format(d,a,b,c))

    return d, a, b, c

class camera:
    def __init__(self,x,y,z,scale):
        self.x = x
        self.y = y
        self.z = z
        self.slope = 0
        self.displace = 100 * scale

        self.x_edges = [[[self.x + self.displace,self.y,self.z + self.displace],[self.x + self.displace,self.y,self.z - self.displace]],[[self.x - self.displace,self.y,self.z + self.displace],[self.x - self.displace,self.y,self.z - self.displace]]]
        self.y_edges = [[[self.x + self.displace, self.y, self.z + self.displace], [self.x - self.displace, self.y, self.z + self.displace]],[[self.x + self.displace, self.y, self.z - self.displace], [self.x - self.displace, self.y, self.z - self.displace]]]

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

            self.screen_point = [(self.vertex_pos[0] + self.t * self.a) + (w/2),self.vertex_pos[1] + self.t * self.b,(self.vertex_pos[2] + self.t * self.c) + (h/2)]

            self.positions.append((self.screen_point[0],self.screen_point[2]))

            #print ("p = {}".format((self.screen_point[0],self.screen_point[2])))
            #print ("--------------------")

            pg.draw.circle(screen,(255,255,255),(int(self.screen_point[0]),int(self.screen_point[2])),2,0)

        pg.draw.line(screen,(100,100,100),self.positions[0],self.positions[1],1)

class vertice:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.distance = 0
    def set_distance(self,distance):
        self.distance = distance
    def get_distance(self):
        return self.distance
    def get_pos(self):
        return self.x,self.y,self.z
    def set_pos(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class cube:
    def __init__(self,scale):
        self.vertices = []
        self.edges = []
        self.pivot_point = [0,0,0]
        self.positions = []

        for x in [-scale,scale]:
            for y in [-scale,scale]:
                for z in [-scale,scale]:
                    self.vertices.append(vertice(x,y,z))
                    self.pivot_point[0] += x
                    self.pivot_point[1] += y
                    self.pivot_point[2] += z
                    self.positions.append((x,y,z))
                    #if len(self.vertices) > 1:
                        #self.edges.append((self.vertices[-1],self.vertices[-2]))

        for self.index in range(0,len(self.vertices)):
            self.vertices[self.index].set_distance(dist(self.vertices[self.index].get_pos(),self.pivot_point))
            for self.i in range(0,len(self.vertices)):
                if self.i != self.index:
                    self.edges.append((self.vertices[self.index],self.vertices[self.i]))


        #self.pivot_point[0] = self.pivot_point[0]/len(self.vertices)
        #self.pivot_point[1] = self.pivot_point[1]/len(self.vertices)
        #self.pivot_point[2] = self.pivot_point[2]/len(self.vertices)
        #print(self.pivot_point)
        self.pivot_point = average(self.positions)

        #for self.index in range(0,len(self.vertices)):
        #    if self.index % 2 == 0:
        #        self.edges.append((self.vertices[self.index],self.vertices[self.index - 1]))

    def rotate(self,velocity):
        for index in range(0,3):
            self.axis = [velocity[0],False,velocity[1]][index]
            print ("axis = {}".format(self.axis))
            if self.axis:
                for self.vertex in self.vertices:
                    self.pos = list(self.vertex.get_pos())
                    self.distance = self.vertex.get_distance()
                    self.rise = self.pos[index - 2] - self.pivot_point[index-2]
                    self.run = self.pos[index - 1] - self.pivot_point[index-1]
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

                    #print ("dist = " + str(self.distance))

                    if self.vertices.index(self.vertex) == 1:
                        print ("{} {}".format(self.vertices.index(self.vertex), self.angle))
                        print (self.pos)
                        print (self.distance)
                        print ("---------------------")

                    self.x = self.pos[0]
                    self.y = self.pos[1]
                    self.z = self.pos[2]

                    #print ("pos = " + str(pos))
                    self.pos[index-2] = self.distance * sin(radians(self.angle))
                    self.pos[index-1] = self.distance * cos(radians(self.angle))
                    #print("pos = " + str(pos))

                    self.vertex.set_pos(self.pos[0],self.pos[1],self.pos[2])

                    pg.draw.line(screen,(255,0,0),(self.pos[index-2],self.pos[index-1]),(self.pivot_point[index-2],self.pivot_point[index-1]),1)


    def display(self):
        for self.edge in self.edges:
            cam.draw_edge(self.edge)

cam = camera(0, 100, 0, 1)
object = cube(50)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0,0,0))

    if pg.mouse.get_pressed()[0] or True:
        #object.rotate(pg.mouse.get_rel())
        object.rotate((1,0))
    object.display()

    pg.display.update()
    clock.tick(60)