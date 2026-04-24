from OpenGL.GL import *
from texture import load_texture
from game_platform import Platform
from enemy import Enemy
from coin import Coin


class Level4:
    """
    Fase 4 - 'Escadaria do Caos'
    Plataformas em formato de escada, alternando subida e descida.
    Buracos longos que forçam uso das plataformas.
    Dificuldade: Difícil
    """

    def __init__(self):
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")

        # Solo com buracos bem longos - quase obriga a usar plataformas
        self.ground_segments = [
            Platform(0,    0, 250, 100),
            Platform(500,  0, 150, 100),
            Platform(900,  0, 150, 100),
            Platform(1300, 0, 150, 100),
            Platform(1700, 0, 300, 100),
        ]

        # Escada subindo e depois descendo
        self.platforms = [
            # Subida
            Platform(120,  160, 100, 20),
            Platform(280,  220, 100, 20),
            Platform(440,  290, 100, 20),
            Platform(600,  360, 100, 20),
            # Topo
            Platform(760,  420, 140, 20),
            # Descida
            Platform(960,  360, 100, 20),
            Platform(1120, 290, 100, 20),
            Platform(1280, 220, 100, 20),
            Platform(1440, 160, 100, 20),
            # Chegada
            Platform(1600, 200, 150, 20),
        ]

        self.enemies = [
            Enemy(self.platforms[1]),
            Enemy(self.platforms[3]),
            Enemy(self.platforms[4]),  # inimigo no topo
            Enemy(self.platforms[6]),
            Enemy(self.platforms[8]),
        ]

        self.coins = [
            Coin(160,  200),
            Coin(320,  260),
            Coin(480,  330),
            Coin(640,  400),
            Coin(800,  460),   # moeda no topo
            Coin(1000, 400),
            Coin(1160, 330),
            Coin(1480, 200),
        ]

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550
        self.end_x = 2000

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
        # Fundo
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.3, 0, 3000, 600)

        # Solo
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments:
            self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        # Plataformas
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms:
            self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)
