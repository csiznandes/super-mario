import glfw #Janela e inputs
from OpenGL.GL import * #Funções gráficas
import time #Calcular delta time, para não depender do FPS
from game import Game
#Definir tamanho da tela
WIDTH = 800
HEIGHT = 600
#Função que é acionada quando o mouse é clicado
def on_mouse_click(window, button, action, mods):
    game = glfw.get_window_user_pointer(window)

    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT: #Somente responde ao clique esquerdo do mouse
        if game.state == 3: #Estado da Loja
            x, y = glfw.get_cursor_pos(window) #Pega a posição do mouse
            mouse_y = HEIGHT - y #Inverte o Y

            #Clique no Botão de Compra
            if 300 <= x <= 500 and 250 <= mouse_y <= 350:
                game.processar_compra_vida()

            #Clique no Botão de Sair
            if 350 <= x <= 450 and 150 <= mouse_y <= 200:
                game.state = 0 #Volta para o menu
                game.reset_game()
#Criação da janela
def init_window():
    if not glfw.init(): #Inicializa GLFW
        return None

    window = glfw.create_window(WIDTH, HEIGHT, "Mickey Bros Python", None, None)

    if not window:
        glfw.terminate()
        return None

    glfw.make_context_current(window)

    #Função de callback de mouse
    glfw.set_mouse_button_callback(window, on_mouse_click)

    return window
#Loop principal
def main():
    window = init_window()
    if not window:
        return
    #Configuração do OpenGL - área de renderização
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #Sistema 2D
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.5, 0.8, 1.0, 1.0)
    #Cria o jogo
    game = Game(WIDTH, HEIGHT)
    #Associação do objeto game à janela
    glfw.set_window_user_pointer(window, game)

    last_time = time.time()
    #Tempo entre frames, que é usado para os movimentos suaves
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