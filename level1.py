from OpenGL.GL import *

from enemy import Enemy
from texture import load_texture
from game_platform import Platform
from player import Player
from ground import criarsolo
from coin import Coin
from goal import Goal
from enemy2 import Enemy2

class Level1:
    def __init__(self):
        # Texturas
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")

        # Player
        self.player = Player()
        self.spawn_x = 100
        self.spawn_y = 150
        self.start()

        # Câmera
        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550

        # Chão
        self.ground_segments = criarsolo()

        # Plataformas
        self.platforms = [
            Platform(200, 200, 120, 20),
            Platform(450, 300, 120, 20),
            Platform(700, 400, 120, 20),

            Platform(1100, 250, 150, 20),
            Platform(1350, 350, 150, 20),
            Platform(1700, 450, 200, 20),
            Platform(2100, 300, 120, 20),

            Platform(2800, 200, 100, 20),
            Platform(3100, 300, 100, 20),
            Platform(3400, 400, 100, 20),
            Platform(3700, 300, 120, 20),
            Platform(4100, 250, 200, 20),
        ]

        # Inimigos
        self.enemies = [
            Enemy(self.platforms[1]),
            Enemy(self.platforms[3]),
            Enemy(self.platforms[5]),
            Enemy(self.platforms[11]),
            Enemy(Platform(1600, 0, 600, 100)),
            Enemy(Platform(3000, 0, 500, 100)),
        ]

        # Inimigos Cano
        self.pipe_enemies = [
            Enemy2(2100, 99),
            Enemy2(3600, 99),
        ]

        # Moedas
        self.coins = [
            Coin(250, 140),
            Coin(700, 450),
            Coin(1350, 400),
            Coin(1700, 500),
            Coin(2100, 350),
            Coin(3400, 450),
            Coin(4100, 300),
            Coin(4600, 150),
        ]

        # Final da fase
        self.finish_line = Goal(4800, 100)

    def start(self):
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.vel_y = 0
        self.player.on_ground = False
        self.camera_x = 0

    def update(self, window, dt, game):
        self.player.update(window, dt)

        self.player.on_ground = False

        # Colisão com chão
        for ground in self.ground_segments:
            ground.check_collision(self.player)

        # Colisão com plataformas
        for platform in self.platforms:
            platform.check_collision(self.player)

        # Moedas
        for coin in self.coins:
            coin.update(dt)
            value = coin.check_collision_with_player(self.player)
            game.score_system.add(value)

        # Inimigos
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.check_collision_with_player(self.player, game)

        for pipe_enemy in self.pipe_enemies:
            pipe_enemy.update(dt)
            pipe_enemy.check_collision_with_player(self.player, game)

        # Câmera
        screen_x = self.player.x - self.camera_x

        if screen_x > self.right_limit:
            self.camera_x = self.player.x - self.right_limit

        if screen_x < self.left_limit:
            self.camera_x = self.player.x - self.left_limit

        if self.camera_x < 0:
            self.camera_x = 0

        # Chegada/final
        if self.finish_line.check_collision(self.player):
            print("VITÓRIA! VOCÊ CHEGOU AO FIM!")
            game.state = 0
            game.reset_game()



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
        self.draw_quad(-self.camera_x * 0.3, 0, 8000, 600)

    def draw_ground(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)

        for ground in self.ground_segments:
            self.draw_quad(
                ground.x - self.camera_x,
                ground.y,
                ground.w,
                ground.h
            )

    def draw_platforms(self):
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.platform_texture)

        for platform in self.platforms:
            self.draw_quad(
                platform.x - self.camera_x,
                platform.y,
                platform.w,
                platform.h
            )

    def draw(self):
        self.draw_background()
        self.draw_ground()
        self.draw_platforms()

        self.finish_line.draw(self.camera_x)

        for coin in self.coins:
            coin.draw(self.camera_x)

        for enemy in self.enemies:
            enemy.draw(self.camera_x)

        for pipe_enemy in self.pipe_enemies:
            pipe_enemy.draw(self.camera_x)

        self.player.draw(self.camera_x)