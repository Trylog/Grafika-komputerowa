import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),

    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)
edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),

    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
)


def frameCube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_QUADS)

    glEnd()

"""
cubeQuads = (
    ()
)



def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


def light():
    glLight(GL_LIGHT0, )  # jest maksymalnie 8 źródeł światła
"""

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glEnable(GL_DEPTH_TEST)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glTranslatef(0.0, 0.5, 0.0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0.0, -0.5, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        frameCube()
        glRotate(1, 1, 1, 1)
        pygame.display.flip()
        pygame.time.wait(5)


main()
