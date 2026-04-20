from OpenGL.GL import *


class Enemy:
    def __init__(self, platform):
        self.w = 20
        self.h = 25

        #inicia o inimigo no topo daas plataformas
        self.y = platform.y + platform.h
        #coloquei ele pra nascer no meio
        self.x = platform.x + (platform.w / 2) - (self.w / 2)

        #limite do movimento
        self.min_x = platform.x
        self.max_x = platform.x + platform.w - self.w

        self.speed = 100
        self.direction = 1  # 1 = direita e -1 = esquerda
        self.ativo = True

    def update(self, dt):
        if not self.ativo:
            return

        # Movimenta o inimigo
        self.x += self.speed * self.direction * dt


        if self.x >= self.max_x:
            self.x = self.max_x
            self.direction = -1


        elif self.x <= self.min_x:
            self.x = self.min_x
            self.direction = 1

    def draw(self, camera_x):
        if not self.ativo:
            return

        screen_x = self.x - camera_x

        #fiz ele ser um bloco, dps tem que pegar uma textura pra ele
        glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(screen_x, self.y)
        glVertex2f(screen_x + self.w, self.y)
        glVertex2f(screen_x + self.w, self.y + self.h)
        glVertex2f(screen_x, self.y + self.h)
        glEnd()

        glColor3f(1.0, 1.0, 1.0)