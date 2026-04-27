from OpenGL.GL import *
from texture import load_texture
from game_platform import Platform
from enemy import Enemy
from coin import Coin


class Level5:
    """
    Fase 5 - 'Castelo Final'
    Fase mais longa e difícil. Quase sem chão, tudo em plataformas.
    Inimigos em quase todas as plataformas.
    Dificuldade: Muito Difícil
    """

    def __init__(self):
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")

        # Chão mínimo - apenas começo e fim
        self.ground_segments = [
            Platform(0,    0, 200, 100),
            Platform(1900, 0, 300, 100),
        ]

        # Layout caótico - exige domínio total do pulo
        self.platforms = [
            # Saída do chão
            Platform(100,  160, 120, 20),
            Platform(280,  230, 100, 20),
            # Primeira sequência alta
            Platform(430,  310, 100, 20),
            Platform(590,  380, 120, 20),
            Platform(760,  310, 100, 20),
            # Descida rápida
            Platform(900,  230, 90,  20),
            Platform(1040, 160, 90,  20),
            # Segunda sequência alta
            Platform(1160, 260, 120, 20),
            Platform(1330, 360, 100, 20),
            Platform(1490, 290, 100, 20),
            Platform(1640, 220, 100, 20),
            # Chegada
            Platform(1800, 160, 150, 20),
        ]

        # Inimigos em quase todas as plataformas
        self.enemies = [
            Enemy(self.platforms[0]),
            Enemy(self.platforms[2]),
            Enemy(self.platforms[3]),
            Enemy(self.platforms[4]),
            Enemy(self.platforms[6]),
            Enemy(self.platforms[7]),
            Enemy(self.platforms[8]),
            Enemy(self.platforms[10]),
        ]

        self.coins = [
            Coin(140,  200),
            Coin(320,  270),
            Coin(470,  350),
            Coin(630,  420),
            Coin(800,  350),
            Coin(940,  270),
            Coin(1080, 200),
            Coin(1200, 300),
            Coin(1370, 400),
            Coin(1530, 330),
            Coin(1680, 260),
            Coin(1840, 200),
        ]

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550
        self.end_x = 2200

    def start(self, player):
        player.x = 80
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
        self.draw_quad(-self.camera_x * 0.3, 0, 3200, 600)

        # Solo (só nas pontas)
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments:
            self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        # Plataformas
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms:
            self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)
