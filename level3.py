from OpenGL.GL import *
from texture import load_texture
from game_platform import Platform
from enemy import Enemy
from coin import Coin


class Level3:
    """
    Fase 3 - 'Céu Estrelado'
    Plataformas mais altas, buracos maiores no solo, mais inimigos.
    Dificuldade: Médio-Difícil
    """

    def __init__(self):
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")

        # Solo com buracos maiores que nas fases anteriores
        self.ground_segments = [
            Platform(0,    0, 300, 100),
            Platform(450,  0, 200, 100),
            Platform(800,  0, 250, 100),
            Platform(1200, 0, 200, 100),
            Platform(1600, 0, 300, 100),
        ]

        # Plataformas suspensas - caminho obrigatório para avançar
        self.platforms = [
            Platform(150, 180, 110, 20),
            Platform(350, 260, 110, 20),
            Platform(560, 340, 110, 20),
            Platform(760, 200, 130, 20),
            Platform(980, 310, 110, 20),
            Platform(1180, 240, 110, 20),
            Platform(1380, 360, 130, 20),
        ]

        self.enemies = [
            Enemy(self.platforms[1]),
            Enemy(self.platforms[3]),
            Enemy(self.platforms[5]),
        ]

        self.coins = [
            Coin(180, 220),
            Coin(390, 300),
            Coin(600, 380),
            Coin(800, 240),
            Coin(1020, 350),
            Coin(1420, 400),
        ]

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550
        self.end_x = 1900

    def start(self, player):
        player.x = 100
        player.y = 150
        player.vel_y = 0
        self.camera_x = 0

    def update(self, player, dt):
        player.on_ground = False

        for g in self.ground_segments:
            g.check_collision(player)

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
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 1); glVertex2f(x, y + h)
        glEnd()

    def draw(self):
        # Fundo com paralaxe
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.3, 0, 2800, 600)

        # Solo
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments:
            self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        # Plataformas
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms:
            self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)
