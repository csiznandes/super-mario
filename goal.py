from OpenGL.GL import *
from texture import load_texture

class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 64
        self.h = 128
        self.texture = load_texture("assets/miney.png") # Crie ou use uma imagem de bandeira

    def check_collision(self, player):
        return (player.x < self.x + self.w and
                player.x + player.w > self.x and
                player.y < self.y + self.h and
                player.y + player.h > self.y)

    def draw(self, camera_x):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        screen_x = self.x - camera_x
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(screen_x, self.y)
        glTexCoord2f(1, 0); glVertex2f(screen_x + self.w, self.y)
        glTexCoord2f(1, 1); glVertex2f(screen_x + self.w, self.y + self.h)
        glTexCoord2f(0, 1); glVertex2f(screen_x, self.y + self.h)
        glEnd()