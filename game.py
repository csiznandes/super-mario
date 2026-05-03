import glfw
from OpenGL.GL import *

from texture import load_texture
from audio import AudioMusica, AudioHitMickey
import numpy as np
from score import Score
from level_random import LevelRandom

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = 0  #0 = menu, 1 = jogando, 2 = vitória, 3 = loja

        #Imagens/texturas
        self.menu_bg = load_texture("assets/background_mickey.png")
        self.title_tex = load_texture("assets/mickey_bros.png")
        self.btn_start_tex = load_texture("assets/start_button.png")
        self.btn_exit_tex = load_texture("assets/exit_button.png")
        self.btn_restart_tex = load_texture("assets/restart_button.png")
        self.win_bg = load_texture("assets/win_bg.png")
        self.btn_menu_tex = load_texture("assets/win_bg.png")

        #Fase
        self.current_level_num = 1
        self.level = LevelRandom(dificuldade=1)

        #Pontuação
        self.score_system = Score(self.width, self.height)

        #Áudio
        # self.musica_fundo = AudioMusica()
        # self.musica_fundo.tocar()
        self.som_hit = AudioHitMickey()

        #Vidas
        self.max_lives = 3
        self.lives = 3
        self.life_texture = load_texture("assets/vida.png")

        self.fall_limit = -150
        self.menu_timer = 0
    #Reseta a posição do jogador
    def reset_player_position(self):
        self.level.start()
    #Jogador perde uma vida
    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.som_hit.tocar()

        self.reset_player_position()
    #Reseta o jogo
    def reset_game(self):
        self.lives = 3
        self.score_system.reset()
        self.current_level_num = 1
        self.level = LevelRandom(dificuldade=1)
        self.level.start()
    #Comprar vida
    def processar_compra_vida(self):
        if self.score_system.score >= 100:
            self.score_system.score -= 100
            self.lives += 1
            self.state = 1
            self.level.start()
        else:
            #Caso ele tente clicar sem ter o valor, manda direto para o menu
            print("Saldo insuficiente. Retornando ao menu...")
            self.state = 0
            self.reset_game()
    #Próxima fase
    def next_level(self):
        self.current_level_num += 1

        if self.current_level_num <= 1:
            self.level = LevelRandom(dificuldade=self.current_level_num)
            self.level.start()
            print(f"\nCHECKPOINT ALCANÇADO")
            print(f"CARREGANDO FASE {self.current_level_num}...")
        else:
            self.state = 2
    #Lógica principal do jogo
    def update(self, window, dt):
        if self.state == 1: #Se está jogando, atualiza fase, verifica queda e morte
            self.level.update(window, dt, self)
            player = self.level.player

            glfw.set_window_title(
                window,
                f"Mickey Bros | FASE: {self.current_level_num} | Score: {self.score_system.score} | Vidas: {self.lives}"
            )
            #Se cair, perde vida
            if player.y < self.fall_limit:
                self.lose_life()

            if self.lives <= 0:
                #Se não tem moedas para comprar vida, volta pro menu direto
                if self.score_system.score < 100:
                    print("SEM VIDAS E SEM MOEDAS - GAME OVER")
                    self.state = 0
                    self.reset_game()
                else:
                    #Se tem moedas, abre a loja
                    print("ABRINDO LOJA DE VIDAS")
                    self.state = 3

        elif self.state == 0:
            self.menu_timer += dt

            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                x_pos, y_pos = glfw.get_cursor_pos(window)
                y_pos = self.height - y_pos
                self.check_menu_clicks(x_pos, y_pos, window)

        elif self.state == 2:
            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                x_pos, y_pos = glfw.get_cursor_pos(window)
                y_pos = self.height - y_pos
                self.check_win_clicks(x_pos, y_pos, window)

    def draw_quad(self, x, y, w, h):
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

    def check_menu_clicks(self, x, y, window):
        x_min = 310
        x_max = 480

        if x_min < x < x_max and 150 < y < 230:
            self.reset_game()
            self.state = 1

        if x_min < x < x_max and 0 < y < 150:
            glfw.set_window_should_close(window, True)

    def check_win_clicks(self, x, y, window):
        #RESTART
        if 300 < x < 500 and 300 < y < 370:
            self.reset_game()
            self.state = 1

        #MENU
        elif 300 < x < 500 and 200 < y < 270:
            self.state = 0

        #EXIT
        elif 300 < x < 500 and 100 < y < 170:
            glfw.set_window_should_close(window, True)

    def draw_win_screen(self):
        glColor3f(1, 1, 1)

        glBindTexture(GL_TEXTURE_2D, self.menu_bg)
        self.draw_quad(0, 0, self.width, self.height)
        #YOU WIN
        glBindTexture(GL_TEXTURE_2D, self.win_bg)
        self.draw_quad(300, 400, 200, 200)
        #botões
        glBindTexture(GL_TEXTURE_2D, self.btn_restart_tex)
        self.draw_quad(300, 300, 200, 70)

        glBindTexture(GL_TEXTURE_2D, self.btn_exit_tex)
        self.draw_quad(300, 200, 200, 70)

    def draw_lives(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.life_texture)

        icon_w = 40
        icon_h = 40
        start_x = 20
        start_y = self.height - 60
        spacing = 10

        for i in range(self.lives):
            x = start_x + i * (icon_w + spacing)
            y = start_y
            self.draw_quad(x, y, icon_w, icon_h)

    def draw_menu(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.menu_bg)
        self.draw_quad(0, 0, self.width, self.height)

        movimento_y = np.sin(self.menu_timer * 2.0) * 15
        movimento_x = np.cos(self.menu_timer * 1.0) * 5

        glBindTexture(GL_TEXTURE_2D, self.title_tex)
        self.draw_quad(102 + movimento_x, 230 + movimento_y, 595, 328)

        glBindTexture(GL_TEXTURE_2D, self.btn_exit_tex)
        self.draw_quad(310, 70, 150, 70)

        glBindTexture(GL_TEXTURE_2D, self.btn_start_tex)
        self.draw_quad(310, 150, 150, 70)

    def draw(self):
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        if self.state == 1:
            self.level.draw()
            self.draw_lives()
            self.score_system.draw()
        elif self.state == 0:
            self.draw_menu()
        elif self.state == 2:
            self.draw_win_screen()
        elif self.state == 3:
            self.level.draw()  #Desenha a fase ao fundo (parada)
            self.level.draw_shop_screen(self.score_system.score)  #Desenha o menu da loja