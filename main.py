import glfw
from OpenGL.GL import *
import time
from game import Game

WIDTH = 800
HEIGHT = 600


def on_mouse_click(window, button, action, mods):
    game = glfw.get_window_user_pointer(window)

    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
        if game.state == 3: #Estado da Loja
            x, y = glfw.get_cursor_pos(window)
            mouse_y = HEIGHT - y #Inverte o Y

            #Clique no Botão de Compra
            if 300 <= x <= 500 and 250 <= mouse_y <= 350:
                game.processar_compra_vida()

            #Clique no Botão de Sair
            if 350 <= x <= 450 and 150 <= mouse_y <= 200:
                game.state = 0 #Volta para o menu
                game.reset_game()

def init_window():
    if not glfw.init():
        return None

    window = glfw.create_window(WIDTH, HEIGHT, "Mickey Bros Python", None, None)

    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)

    #Função de callback de mouse
    glfw.set_mouse_button_callback(window, on_mouse_click)

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

    glfw.set_window_user_pointer(window, game)

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