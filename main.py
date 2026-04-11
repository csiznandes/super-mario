import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import time

from player import Player
from texture import load_texture
from game_platform import Platform

WIDTH = 800
HEIGHT = 600

def init_window():
    if not glfw.init():
        return None

    window = glfw.create_window(WIDTH, HEIGHT, "Super Mario Python", None, None)

    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)
    return window


def draw_quad(x, y, w, h):

    glBegin(GL_QUADS)

    glTexCoord2f(0, 0)
    glVertex2f(x, y)

    glTexCoord2f(1, 0)
    glVertex2f(x + w, y)

    glTexCoord2f(1, 1)
    glVertex2f(x + w, y + h)

    glTexCoord2f(0, 1)
    glVertex2f(x, y + h)

    glEnd()


def main():

    window = init_window()

    glViewport(0, 0, WIDTH, HEIGHT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)

    mario_texture = load_texture("assets/mickey.png")
    background_texture = load_texture("assets/background_mickey.png")

    player = Player()

    platforms = [
        Platform(0, 0, 800, 100),
        Platform(200, 200, 120, 20),
        Platform(400, 300, 120, 20),
        Platform(600, 400, 120, 20)
    ]

    last_time = time.time()

    while not glfw.window_should_close(window):

        current_time = time.time()
        delta = current_time - last_time
        last_time = current_time

        glfw.poll_events()

        player.update(window, delta)

        #Reseta o chão
        player.on_ground = False

        #Verifica a colisão com plataformas
        for p in platforms:
            p.check_collision(player)

        glClear(GL_COLOR_BUFFER_BIT)

        #Desenha o fundo
        glBindTexture(GL_TEXTURE_2D, background_texture)
        draw_quad(0, 0, WIDTH, HEIGHT)

        #Desenha as plataformas
        glBindTexture(GL_TEXTURE_2D, 0)

        for p in platforms:

            glBegin(GL_QUADS)
            glColor3f(0.6, 0.3, 0.1)

            glVertex2f(p.x, p.y)
            glVertex2f(p.x + p.w, p.y)
            glVertex2f(p.x + p.w, p.y + p.h)
            glVertex2f(p.x, p.y + p.h)

            glEnd()

        glColor3f(1,1,1)

        #Desenha o jogador
        glBindTexture(GL_TEXTURE_2D, mario_texture)
        draw_quad(player.x, player.y, 64, 64)

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()