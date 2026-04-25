import glfw
from OpenGL.GL import *

from texture import load_texture
from audio import AudioMusica, AudioHitMickey
import numpy as np
from score import Score
from level1 import Level1


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = 0  # 0 = menu, 1 = jogando

        # Menu
        self.menu_bg = load_texture("assets/background_mickey.png")
        self.title_tex = load_texture("assets/mickey_bros.png")
        self.btn_start_tex = load_texture("assets/start_button.png")
        self.btn_exit_tex = load_texture("assets/exit_button.png")

        # Fase
        self.level = Level1()

        # Score
        self.score_system = Score(self.width, self.height)

        # Áudio
        self.musica_fundo = AudioMusica()
        self.musica_fundo.tocar()

        self.som_hit = AudioHitMickey()

        # Vidas
        self.max_lives = 3
        self.lives = 3
        self.life_texture = load_texture("assets/vida.png")

        self.fall_limit = -150
        self.menu_timer = 0

    def reset_player_position(self):
        self.level.start()

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.som_hit.tocar()

        self.reset_player_position()

    def reset_game(self):
        self.lives = 3
        self.score_system.reset()
        self.level = Level1()
        self.level.start()

    def update(self, window, dt):
        if self.state == 1:
            self.level.update(window, dt, self)

            player = self.level.player

            glfw.set_window_title(
                window,
                f"Mickey Bros - Score: {self.score_system.score}  Vidas: {self.lives}"
            )

            if player.y < self.fall_limit:
                self.lose_life()

            if self.lives <= 0:
                print("GAME OVER")
                self.state = 0
                self.reset_game()

        elif self.state == 0:
            self.menu_timer += dt

            if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
                x_pos, y_pos = glfw.get_cursor_pos(window)
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

    def check_menu_clicks(self, x, y, window):
        x_min = self.width / 2 - 150
        x_max = self.width / 2 + 150

        if x_min < x < x_max and 150 < y < 230:
            self.reset_game()
            self.state = 1

        if x_min < x < x_max and 70 < y < 150:
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
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.menu_bg)
        self.draw_quad(0, 0, self.width, self.height)

        movimento_y = np.sin(self.menu_timer * 2.0) * 15
        movimento_x = np.cos(self.menu_timer * 1.0) * 5

        glBindTexture(GL_TEXTURE_2D, self.title_tex)
        self.draw_quad(102 + movimento_x, 230 + movimento_y, 595, 328)

        glBindTexture(GL_TEXTURE_2D, self.btn_start_tex)
        self.draw_quad(0, -115, self.width, self.height)

        glBindTexture(GL_TEXTURE_2D, self.btn_exit_tex)
        self.draw_quad(0, -185, self.width, self.height)

    def draw(self):
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        if self.state == 1:
            self.level.draw()
            self.draw_lives()
            self.score_system.draw()
        else:
            self.draw_menu()