import glfw
from OpenGL.GL import *

from player import Player
from texture import load_texture
from game_platform import Platform
from ground import criarsolo


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player()

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

        self.spawn_x = 100
        self.spawn_y = 150

        self.player.x = self.spawn_x
        self.player.y = self.spawn_y

        self.fall_limit = -150

    def reset_player_position(self):
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.vel_y = 0
        self.player.on_ground = False
        self.camera_x = 0

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
        self.reset_player_position()

    def update(self, window, dt):
        self.player.update(window, dt)

        self.player.on_ground = False

        # colisão com solo
        for ground in self.ground_segments:
            ground.check_collision(self.player)

        # colisão com plataformas
        for platform in self.platforms:
            platform.check_collision(self.player)

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
            self.lives += 3
            #chamada da tela de game over



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

    def draw(self):
        glLoadIdentity()

        self.draw_background()
        self.draw_ground()
        self.draw_platforms()

        glColor3f(1, 1, 1)
        self.player.draw(self.camera_x)

        self.draw_lives()