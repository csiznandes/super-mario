import glfw
from OpenGL.GL import *
from enemy import Enemy
from texture import load_texture
from game_platform import Platform
from player import Player
from ground import criarsolo
from coin import Coin
from goal import Goal
from enemy2 import Enemy2

class Level2:
    def __init__(self):
        # Texturas
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")

        # Player
        self.player = Player()
        # Removi o aumento excessivo de gravidade para facilitar o acesso às plataformas
        self.player.gravity = 1000
        self.player.jump_force = 500

        self.spawn_x = 100
        self.spawn_y = 150
        self.start()

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550

        # --- ESTRUTURA DO MAPA AJUSTADA (Mais próxima) ---

        # Segmentos de Solo Firme
        # Reduzi a distância entre solos de 400px para ~200px onde não há plataformas auxiliares
        self.ground_segments = [
            Platform(0, 0, 400, 100),       # Início
            Platform(650, 0, 300, 100),     # Ilha 1 (Antes era em 800)
            Platform(1200, 0, 400, 100),    # Ilha 2 (Antes era em 1500)
            Platform(2100, 0, 600, 100),    # Plataforma longa (Antes era em 2400)
            Platform(3100, 0, 300, 100),    # Penúltimo suporte (Antes era em 3500)
            Platform(4000, 0, 800, 100)     # SOLO FINAL DA MINEY (Mais longo para segurança)
        ]

        # Plataformas Suspensas (Pontes entre os solos)
        self.platforms = [
            # Preenchendo o buraco entre solo 1 e solo 2
            Platform(450, 150, 100, 25),
            Platform(550, 220, 100, 25),

            # Subida para moedas e transição para solo 3
            Platform(1000, 180, 100, 25),
            Platform(1150, 280, 80, 20),

            # Sequência entre solo 3 e solo 4 (Ponte de plataformas)
            Platform(1650, 150, 120, 25),
            Platform(1800, 250, 100, 25),
            Platform(1950, 320, 100, 25),

            # Entre solo 4 e solo 5
            Platform(2750, 180, 120, 25),
            Platform(2920, 250, 100, 25),

            # Reta final para o Solo da Miney
            Platform(3450, 200, 100, 25),
            Platform(3600, 300, 100, 25),
            Platform(3800, 220, 120, 25),
        ]

        # Inimigos ajustados para as novas posições
        self.enemies = [
            Enemy(self.ground_segments[2]),
            Enemy(self.ground_segments[3]),
            Enemy(self.platforms[5]),
            Enemy(self.ground_segments[5]),
        ]

        self.pipe_enemies = [
            Enemy2(1250, 99),
            Enemy2(2300, 99),
            Enemy2(4200, 99),
        ]

        # Moedas posicionadas como "guia" de salto
        self.coins = [
            Coin(500, 200),
            Coin(1180, 330),
            Coin(1850, 300),
            Coin(2800, 250),
            Coin(3650, 350),
            Coin(4100, 150),
            Coin(4150, 150),
        ]

        # Miney posicionada no final do solo expandido
        self.finish_line = Goal(4500, 100)

    def start(self):
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.vel_y = 0
        self.player.on_ground = False
        self.camera_x = 0

    def update(self, window, dt, game):
        self.player.update(window, dt)
        self.player.y += self.player.vel_y * dt
        self.player.on_ground = False

        for ground in self.ground_segments: ground.check_collision(self.player)
        for platform in self.platforms: platform.check_collision(self.player)

        for coin in self.coins:
            coin.update(dt)
            game.score_system.add(coin.check_collision_with_player(self.player))

        for enemy in self.enemies:
            enemy.update(dt)
            enemy.check_collision_with_player(self.player, game)

        for pe in self.pipe_enemies:
            pe.update(dt)
            pe.check_collision_with_player(self.player, game)

        # Câmera segue o Mickey
        screen_x = self.player.x - self.camera_x
        if screen_x > self.right_limit: self.camera_x = self.player.x - self.right_limit
        if screen_x < self.left_limit: self.camera_x = self.player.x - self.left_limit

        if self.camera_x < 0: self.camera_x = 0
        # Ajuste do limite da câmera para o novo final
        if self.camera_x > 4000: self.camera_x = 4000

        if self.finish_line.check_collision(self.player):
            game.state = 2

    def draw_quad(self, x, y, w, h):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + w, y)
        glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
        glTexCoord2f(0, 1); glVertex2f(x, y + h)
        glEnd()

    def draw(self):
        # Background
        glColor3f(0.6, 0.5, 0.8)
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.2, 0, 6000, 600)

        glColor3f(1, 1, 1)
        # Desenhar Solo
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments:
            self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        # Desenhar Plataformas
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms:
            self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)

        self.finish_line.draw(self.camera_x)
        for c in self.coins: c.draw(self.camera_x)
        for e in self.enemies: e.draw(self.camera_x)
        for pe in self.pipe_enemies: pe.draw(self.camera_x)
        self.player.draw(self.camera_x)