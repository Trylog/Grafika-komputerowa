import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    cube_rotation = 0
    camera_translation = [0, 0, 0]
    camera_rotation = [0, 0, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    # Przesuń kamerę do przodu z uwzględnieniem aktualnego obrotu
                    camera_translation[0] -= 0.1 * math.sin(math.radians(camera_rotation[1]))
                    camera_translation[2] += 0.1 * math.cos(math.radians(camera_rotation[1]))
                elif event.key == pygame.K_s:
                    # Przesuń kamerę do tyłu z uwzględnieniem aktualnego obrotu
                    camera_translation[0] += 0.1 * math.sin(math.radians(camera_rotation[1]))
                    camera_translation[2] -= 0.1 * math.cos(math.radians(camera_rotation[1]))
                elif event.key == pygame.K_a:
                    # Przesuń kamerę w lewo z uwzględnieniem aktualnego obrotu
                    camera_translation[0] += 0.1 * math.cos(math.radians(camera_rotation[1]))
                    camera_translation[2] += 0.1 * math.sin(math.radians(camera_rotation[1]))
                elif event.key == pygame.K_d:
                    # Przesuń kamerę w prawo z uwzględnieniem aktualnego obrotu
                    camera_translation[0] -= 0.1 * math.cos(math.radians(camera_rotation[1]))
                    camera_translation[2] -= 0.1 * math.sin(math.radians(camera_rotation[1]))
                elif event.key == pygame.K_q:
                    camera_rotation[1] += 5
                elif event.key == pygame.K_e:
                    camera_rotation[1] -= 5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        glTranslatef(*camera_translation)
        glRotatef(camera_rotation[0], 1, 0, 0)
        glRotatef(camera_rotation[1], 0, 1, 0)

        glPushMatrix()
        glRotatef(cube_rotation, 1, 1, 1)
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)
        cube_rotation += 1

if __name__ == "__main__":
    main()
