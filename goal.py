from OpenGL.GL import *
from texture import load_texture
#Objetivo, final da fase (Miney)
class Goal:
    def __init__(self, x, y): #Recebe posição inicial
        #Posição no mundo
        self.x = x
        self.y = y
        #Tamanho da imagem da Miney
        self.w = 90
        self.h = 128
        self.texture = load_texture("assets/miney.png")
    #Colisão AABB
    def check_collision(self, player):
        return (player.x < self.x + self.w and
                player.x + player.w > self.x and
                player.y < self.y + self.h and
                player.y + player.h > self.y)
    #Desenha a imagem
    def draw(self, camera_x):
        glBindTexture(GL_TEXTURE_2D, self.texture)
        screen_x = self.x - camera_x
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(screen_x, self.y)
        glTexCoord2f(1, 0); glVertex2f(screen_x + self.w, self.y)
        glTexCoord2f(1, 1); glVertex2f(screen_x + self.w, self.y + self.h)
        glTexCoord2f(0, 1); glVertex2f(screen_x, self.y + self.h)
        glEnd()