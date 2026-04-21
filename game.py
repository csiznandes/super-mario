import glfw
from OpenGL.GL import *

from game_platform import Platform
from ground import criarsolo
from player import Player
from texture import load_texture
from audio import AudioMusica, AudioHit
from enemy import Enemy
import numpy as np

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = 0 #Estados do jogo: 0 = menu/lobby, 1 = jogando
        #Carregar texturas do Menu (certifique-se de ter esses arquivos)
        self.menu_bg = load_texture("assets/background_mickey.png")
        self.title_tex = load_texture("assets/mickey_bros.png")
        self.btn_start_tex = load_texture("assets/start_button.png")
        self.btn_exit_tex = load_texture("assets/exit_button.png")

        self.player = Player()

        self.musica_fundo = AudioMusica()
        self.musica_fundo.tocar()
        self.som_hit = AudioHit()

        self.max_lives = 3
        self.lives = 3
        self.life_texture = load_texture("assets/vida.png")

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550

        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")
        # SOLO COM BURACOS
        self.ground_segments = criarsolo()

        # PLATAFORMAS SUSPENSAS
        self.platforms = [
            Platform(200, 200, 120, 20),
            Platform(400, 300, 120, 20),
            Platform(600, 400, 120, 20),
            Platform(900, 250, 120, 20),
            Platform(1200, 350, 120, 20),
        ]

        self.enemies = [
            Enemy(self.platforms[1]),
            Enemy(self.platforms[2])
        ]

        self.spawn_x = 100
        self.spawn_y = 150

        self.player.x = self.spawn_x
        self.player.y = self.spawn_y

        self.fall_limit = -150

        self.menu_timer = 0

    def reset_player_position(self):
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.vel_y = 0
        self.player.on_ground = False
        self.camera_x = 0

    def lose_life(self):
        self.som_hit = AudioHit()
        if self.lives > 0:
            self.lives -= 1
        self.reset_player_position()

    def reset_game(self):
        self.lives = 3
        self.reset_player_position()
        for enemy in self.enemies:
            enemy.ativo = True

    def update(self, window, dt):
        if self.state == 1:  #JOGANDO

            self.player.update(window, dt)

            self.player.on_ground = False

            #colisão com solo
            for ground in self.ground_segments:
                ground.check_collision(self.player)

            #colisão com plataformas
            for platform in self.platforms:
                platform.check_collision(self.player)

            #Update e Colisão dos inimigos
            for enemy in self.enemies:
                enemy.update(dt)

                if enemy.ativo:

                    if (self.player.x < enemy.x + enemy.w and
                            self.player.x + self.player.w > enemy.x and
                            self.player.y < enemy.y + enemy.h and
                            self.player.y + self.player.h > enemy.y):

                        #onde ve se foi por cima
                        if self.player.vel_y < 0 and self.player.y > enemy.y + (enemy.h * 0.5):
                            enemy.ativo = False  # Mata o inimigo
                            self.player.vel_y = self.player.jump_force * 0.8 #achei que ficou legal subir
                            # o player dps de acertar o bicho, qualquer coisa da pra tirar
                        else:
                            self.lose_life()

            screen_x = self.player.x - self.camera_x

            if screen_x > self.right_limit:
                self.camera_x = self.player.x - self.right_limit

            if screen_x < self.left_limit:
                self.camera_x = self.player.x - self.left_limit

            if self.camera_x < 0:
                self.camera_x = 0

            if self.player.y < self.fall_limit:
                self.lose_life()

            if self.lives <= 0:
                print("GAME OVER")
                #self.lives += 3
                self.state = 0
                #chamada da tela de game over
                self.reset_player_position()
                self.lives = 3  #Reseta as vidas para o próximo round

        elif self.state == 0:  # NO MENU
            self.menu_timer += dt
            #Lógica para detectar clique do mouse
            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                x_pos, y_pos = glfw.get_cursor_pos(window)
                #Inverter o Y (GLFW topo=0, OpenGL base=0)
                y_pos = self.height - y_pos
                self.check_menu_clicks(x_pos, y_pos, window)

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

    def draw_background(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.3, 0, self.width * 3, self.height)

    def draw_ground(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)

        for g in self.ground_segments:
            self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

    def draw_platforms(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)

        for p in self.platforms:
            self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)

    def check_menu_clicks(self, x, y, window):
        x_min = self.width / 2 - 150
        x_max = self.width / 2 + 150

        #Botão INICIAR
        if (x_min < x < x_max and 150 < y < 230):
            self.reset_game()
            self.state = 1

        #Botão SAIR
        if (x_min < x < x_max and 70 < y < 150):
            glfw.set_window_should_close(window, True)

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
        #Desenha o Fundo
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.menu_bg)
        self.draw_quad(0, 0, self.width, self.height)

        #EFEITO PARALAXE COM NUMPY: np.sin e np.cos fazem o letreiro flutuar
        movimento_y = np.sin(self.menu_timer * 2.0) * 15
        movimento_x = np.cos(self.menu_timer * 1.0) * 5

        #Desenha o Letreiro com o movimento
        glBindTexture(GL_TEXTURE_2D, self.title_tex)
        self.draw_quad(102 + movimento_x, 230 + movimento_y, 595, 328)

        #Desenha os Botões (fixos para facilitar o clique)
        glBindTexture(GL_TEXTURE_2D, self.btn_start_tex)
        self.draw_quad(0, -115, self.width, self.height)

        glBindTexture(GL_TEXTURE_2D, self.btn_exit_tex)
        self.draw_quad(0, -185, self.width, self.height)

    def draw(self):
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)  #Garante que a tela seja limpa

        if self.state == 1:
            #Desenha o jogo
            self.draw_background()
            self.draw_ground()
            self.draw_platforms()
            for enemy in self.enemies:
                enemy.draw(self.camera_x)
            self.player.draw(self.camera_x)
            self.draw_lives()
        else:
            #Desenha apenas o menu
            self.draw_menu()