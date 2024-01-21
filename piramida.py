import math

import pygame
from OpenGL.raw.GLUT import glutSolidSphere
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

light_angle = 0.0

ground_vertices = (
    (-10, -1 / 3, -10),
    (-10, -1 / 3, 10),
    (10, -1 / 3, 10),
    (10, -1 / 3, -10),
)


vertices = [
    [-0.5, -1 / 3, -1 / 3],
    [0.5, -1 / 3, -1 / 3],
    [0, -1 / 3, 2 / 3],
    [0, 2 / 3, 0],
]
edges = [
    (0, 1),
    (1, 2),
    (2, 0),
    (3, 0),
    (3, 1),
    (3, 2),
]

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001


def startup():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image = Image.open("tekstura.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
    #glTexCoord2f

def avg(q1, q2):
    return (q1 + q2) / 2


def avgC(p1, p2):
    return [avg(p1[0], p2[0]), avg(p1[1], p2[1]), avg(p1[2], p2[2])]


def subPyramid(a, b, c, d, depth):
    fP = len(vertices)
    ab = avgC(a, b)  # 0
    bc = avgC(b, c)  # 1
    ca = avgC(c, a)  # 2
    ad = avgC(a, d)  # 3
    bd = avgC(b, d)  # 4
    cd = avgC(c, d)  # 5

    vertices.append(ab)
    vertices.append(bc)
    vertices.append(ca)
    vertices.append(ad)
    vertices.append(bd)
    vertices.append(cd)

    edges.append((fP, fP + 2))
    edges.append((fP, fP + 3))
    edges.append((fP + 2, fP + 3))

    edges.append((fP, fP + 1))
    edges.append((fP, fP + 4))
    edges.append((fP + 1, fP + 4))

    edges.append((fP + 1, fP + 2))
    edges.append((fP + 1, fP + 5))
    edges.append((fP + 2, fP + 5))

    edges.append((fP + 3, fP + 4))
    edges.append((fP + 4, fP + 5))
    edges.append((fP + 5, fP + 3))

    if depth != 0:
        depth -= 1

        subPyramid(a, ab, ca, ad, depth)
        subPyramid(ab, b, bc, bd, depth)
        subPyramid(ca, bc, c, cd, depth)
        subPyramid(ad, bd, cd, d, depth)


def pyramid():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def ground():
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glVertex3fv(vertex)
    glEnd()


def update_light_position():

    global light_angle
    light_radius = 3.0
    light_x = light_radius * math.cos(math.radians(light_angle))
    light_y = light_radius * math.sin(math.radians(light_angle))
    light_position1 = [light_x, light_y, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position1)
    light_angle += 0.2


def main():
    #pygame.init()

    display = (1500, 850)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(90, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -2)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_position1 = [1.0, 1.0, 1.0, 0.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glScalef(1, 1, -1)

    subPyramid([-0.5, -1 / 3, -1 / 3],
               [0.5, -1 / 3, -1 / 3],
               [0, -1 / 3, 2 / 3],
               [0, 2 / 3, 0], 3)
    print(len(edges))
    startup()
    camera_translation = [0, 0, 0]
    camera_rotation = [0, 0, 0]
    pyramid_rotation_d = 0
    pyramid_rotation_xyz = [0, 1, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    camera_translation[2] += 0.5
                if event.key == pygame.K_s:
                    camera_translation[2] -= 0.5
                if event.key == pygame.K_a:
                    camera_translation[0] += 0.5
                if event.key == pygame.K_d:
                    camera_translation[0] -= 0.5
                if event.key == pygame.K_SPACE:
                    camera_translation[1] -= 0.5
                if event.key == pygame.K_LSHIFT:
                    camera_translation[1] += 0.5
                if event.key == pygame.K_e:
                    camera_rotation[1] += 5
                if event.key == pygame.K_q:
                    camera_rotation[1] -= 5
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluPerspective(90, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(*camera_translation)
        glRotatef(camera_rotation[0], 1, 0, 0)
        glRotatef(camera_rotation[1], 0, 1, 0)

        glPushMatrix()
        ground()
        #glRotatef(pyramid_rotation_d, *pyramid_rotation_xyz)
        pyramid()
        glPopMatrix()

        update_light_position()
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glTranslatef(light_position1[0], light_position1[1], light_position1[2])
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.1, 10, 10)
        glPopMatrix()
        glEnable(GL_LIGHTING)  # Włącz oświetlenie z powrotem

        #glLightfv(GL_LIGHT0, GL_POSITION, )

        # glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        # glBegin(GL_TRIANGLES)
        # glTexCoord2f(0.0, 0.0)
        # glVertex3f(-5.0, -5.0, 0.0)
        # glTexCoord2f(1.0, 0.0)
        # glVertex3f(5.0, -5.0, 0.0)
        # glTexCoord2f(0.5, 1.0)
        # glVertex3f(0.0, 5.0, 0.0)
        # glEnd()

        # glLoadIdentity()
        #light_position[2] = light_position[2] - 0.1
        # glTranslatef(x, y, z)
        pygame.display.flip()
        pygame.time.wait(10)
        pyramid_rotation_d += 1


main()
