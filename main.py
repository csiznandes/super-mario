import glfw
from OpenGL.GL import *
import time

from game import Game

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


def main():
    window = init_window()
    if not window:
        return

    glViewport(0, 0, WIDTH, HEIGHT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.8, 1.0, 1.0)

    game = Game(WIDTH, HEIGHT)

    last_time = time.time()

    while not glfw.window_should_close(window):
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        glfw.poll_events()

        game.update(window, dt)

        glClear(GL_COLOR_BUFFER_BIT)
        game.draw()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()