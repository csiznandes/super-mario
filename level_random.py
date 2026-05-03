
import random
from OpenGL.GL import *
from enemy import Enemy
from texture import load_texture
from game_platform import Platform
from player import Player
from ground import criarsolo
from coin import Coin
from goal import Goal
from enemy2 import Enemy2

class LevelRandom:
    def __init__(self, dificuldade=1):
        self.dificuldade = dificuldade
        # Texturas (mantenha o seu código de carregar texturas aqui)
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")
        self.btn_restart_tex = load_texture("assets/restart_button.png")
        self.btn_exit_tex = load_texture("assets/exit_button.png")

        self.player = Player()
        self.spawn_x = 100
        self.spawn_y = 150

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550

        # Listas vazias para preencher aleatoriamente
        self.ground_segments = [Platform(0, 0, 400, 100)]  # Início sempre seguro
        self.platforms = []
        self.enemies = []
        self.coins = []

        self.gerar_fase_aleatoria()
        self.start()

    def gerar_fase_aleatoria(self):
        distancia_atual = 400
        comprimento_total = 3000 + (self.dificuldade * 1000)

        # Variável crucial para evitar saltos impossíveis
        altura_anterior = 0

        while distancia_atual < comprimento_total:
            # 1. BURACO: Reduzi o máximo para 160 para garantir que o pulo alcance
            buraco = random.randint(100, 160)
            distancia_atual += buraco

            # 2. ALTURA RELATIVA:
            # O Mickey só consegue subir uma certa altura em relação à última plataforma.
            # Vamos limitar a variação de altura para no máximo 120 pixels para cima.
            variacao_maxima = 120
            min_altura = max(0, altura_anterior - 150)  # Pode descer bastante
            max_altura = min(250, altura_anterior + variacao_maxima)  # Mas sobe pouco

            altura = random.randint(min_altura, max_altura)
            largura = random.randint(200, 400)

            nova_plataforma = Platform(distancia_atual, altura, largura, 25 if altura > 0 else 100)

            if altura == 0:
                self.ground_segments.append(nova_plataforma)
            else:
                self.platforms.append(nova_plataforma)

            # Atualiza a altura para a próxima iteração saber de onde o Mickey vem
            altura_anterior = altura

            # 3. INIMIGOS E MOEDAS
            if random.random() < (0.2 + (self.dificuldade * 0.1)):
                self.enemies.append(Enemy(nova_plataforma))

            if random.random() > 0.5:
                self.coins.append(Coin(distancia_atual + (largura / 2), altura + 60))

            distancia_atual += largura

        # 5. Final da fase
        self.finish_line = Goal(distancia_atual + 200, 100)
        self.ground_segments.append(Platform(distancia_atual + 150, 0, 600, 100))

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

        # Câmera segue o Mickey
        screen_x = self.player.x - self.camera_x
        if screen_x > self.right_limit: self.camera_x = self.player.x - self.right_limit
        if screen_x < self.left_limit: self.camera_x = self.player.x - self.left_limit
        if self.camera_x < 0: self.camera_x = 0

        if self.finish_line.check_collision(self.player):
            game.next_level()

    def draw(self):
        # Background
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.2, 0, 8000, 600)

        # Solo e Plataformas
        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments: self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms: self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)

        self.finish_line.draw(self.camera_x)
        for c in self.coins: c.draw(self.camera_x)
        for e in self.enemies: e.draw(self.camera_x)
        self.player.draw(self.camera_x)

    def draw_quad(self, x, y, w, h):
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0);
        glVertex2f(x, y)
        glTexCoord2f(1, 0);
        glVertex2f(x + w, y)
        glTexCoord2f(1, 1);
        glVertex2f(x + w, y + h)
        glTexCoord2f(0, 1);
        glVertex2f(x, y + h)
        glEnd()