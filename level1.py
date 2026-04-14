from OpenGL.GL import *
from texture import load_texture
from game_platform import Platform

class Level1:
    def __init__(self):
        self.background_texture = load_texture("assets/background_mickey.png")

        self.platforms = [
            Platform(0, 0, 800, 100),
            Platform(200, 200, 120, 20),
            Platform(400, 300, 120, 20),
            Platform(700, 250, 120, 20),
            Platform(1000, 350, 120, 20),
        ]

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550
        self.end_x = 1400

    def start(self, player):
        player.x = 100
        player.y = 100
        player.vel_y = 0
        self.camera_x = 0

    def update(self, player, dt):
        player.on_ground = False

        for p in self.platforms:
            p.check_collision(player)

        screen_x = player.x - self.camera_x

        if screen_x > self.right_limit:
            self.camera_x = player.x - self.right_limit

        if screen_x < self.left_limit:
            self.camera_x = player.x - self.left_limit

        if self.camera_x < 0:
            self.camera_x = 0

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

    def draw(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.3, 0, 2400, 600)

        glBindTexture(GL_TEXTURE_2D, 0)
        glColor3f(0.6, 0.3, 0.1)

        for p in self.platforms:
            glBegin(GL_QUADS)
            glVertex2f(p.x - self.camera_x, p.y)
            glVertex2f(p.x + p.w - self.camera_x, p.y)
            glVertex2f(p.x + p.w - self.camera_x, p.y + p.h)
            glVertex2f(p.x - self.camera_x, p.y + p.h)
            glEnd()