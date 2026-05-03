import random
from OpenGL.GL import *
from enemy import Enemy
from texture import load_texture
from game_platform import Platform
from player import Player
from coin import Coin
from goal import Goal
from enemy2 import Enemy2

class LevelRandom:
    def __init__(self, dificuldade=1):
        self.dificuldade = dificuldade
        self.background_texture = load_texture("assets/background_mickey.png")
        self.platform_texture = load_texture("assets/plataforma.png")
        self.solo_texture = load_texture("assets/gramado.png")
        self.btn_restart_tex = load_texture("assets/restart_button.png")
        self.btn_exit_tex = load_texture("assets/exit_button.png")
        self.btn_buy_life_tex = load_texture("assets/buy_life_button.png")
        #Criação de um jogador
        self.player = Player()
        self.spawn_x = 100
        self.spawn_y = 150

        self.camera_x = 0
        self.left_limit = 250
        self.right_limit = 550

        self.ground_segments = [Platform(0, 0, 400, 100)]
        self.platforms = []
        self.enemies = []
        self.enemies2 = []
        self.coins = []

        self.gerar_fase_aleatoria()
        self.start()

    def gerar_fase_aleatoria(self):
        #Comprimento da fase
        distancia_atual = 400
        comprimento_total = 5000 + (self.dificuldade * 2000) #Fase maior, dificuldade maior
        altura_anterior = 0

        while distancia_atual < comprimento_total:
            #Sorteio de Solo vs Plataforma
            tipo_segmento = random.random()

            if tipo_segmento < 0.6:  #Solo
                altura = 0
                largura = random.randint(400, 800)
                buraco = random.randint(100, 150)
            else:  #Plataforma suspensa
                variacao_maxima = 120
                min_altura = max(50, altura_anterior - 100)
                max_altura = min(220, altura_anterior + variacao_maxima)
                altura = random.randint(min_altura, max_altura)
                largura = random.randint(200, 400)
                buraco = random.randint(120, 160)

            distancia_atual += buraco


            altura_visual = 25 if altura > 0 else 100
            nova_plataforma = Platform(distancia_atual, altura, largura, altura_visual) #Cria plataforma

            if altura == 0:
                self.ground_segments.append(nova_plataforma)
            else:
                self.platforms.append(nova_plataforma)

            #Geração de inimigos
            if random.random() < (0.2 + (self.dificuldade * 0.05)):
                if largura > 150 and random.random() < 0.4:
                    pos_x = distancia_atual + (largura / 2) - 37
                    #O cano nasce no topo da plataforma (altura + h). Se for solo (altura 0), ele ficará em y=100. Se for plataforma suspensa, ele ficará em y=altura+25.
                    self.enemies2.append(Enemy2(pos_x, altura + nova_plataforma.h))
                else:
                    self.enemies.append(Enemy(nova_plataforma))

            #Geração de moedas
            if random.random() > 0.4:
                #Moedas também ficam mais altas se houver um cano
                offset_moeda = 180 if largura > 150 else 60
                self.coins.append(Coin(distancia_atual + (largura / 2), altura + nova_plataforma.h + offset_moeda))

            altura_anterior = altura
            distancia_atual += largura

        #Final da fase
        self.finish_line = Goal(distancia_atual + 200, 100)
        self.ground_segments.append(Platform(distancia_atual + 150, 0, 1000, 100))

    def start(self):
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.vel_y = 0
        self.player.on_ground = False
        self.camera_x = 0
    #Move jogador, aplica gravidade, colisões e a câmera segue o jogador
    def update(self, window, dt, game):
        self.player.update(window, dt)
        self.player.y += self.player.vel_y * dt
        self.player.on_ground = False

        #Colisões com plataformas
        for ground in self.ground_segments: ground.check_collision(self.player)
        for platform in self.platforms: platform.check_collision(self.player)

        #Colisão de Moedas
        for coin in self.coins:
            coin.update(dt)
            game.score_system.add(coin.check_collision_with_player(self.player))

        #Colisão de Inimigos Comuns
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.check_collision_with_player(self.player, game)

        #Colisão do Bafo no Cano
        for enemy2 in self.enemies2:
            enemy2.update(dt)
            enemy2.check_collision_with_player(self.player, game)

        #Câmera
        screen_x = self.player.x - self.camera_x
        if screen_x > self.right_limit: self.camera_x = self.player.x - self.right_limit
        if screen_x < self.left_limit: self.camera_x = self.player.x - self.left_limit
        if self.camera_x < 0: self.camera_x = 0

        if self.finish_line.check_collision(self.player):
            game.next_level()

    def draw_shop_screen(self, current_coins):
        #Escurece um pouco o fundo
        glDisable(GL_TEXTURE_2D)
        glColor4f(0, 0, 0, 0.7)
        self.draw_quad(0, 0, 800, 600)
        glColor4f(1, 1, 1, 1)
        glEnable(GL_TEXTURE_2D)

        #Desenha o botão de "Comprar Vida" no centro da tela. Se o jogador tiver moedas, ele aparece normal, se não, pode aparecer opaco
        if current_coins >= 100:
            glColor4f(1, 1, 1, 1)
        else:
            glColor4f(0.5, 0.5, 0.5, 1)  #Tom cinza se não puder comprar

        glBindTexture(GL_TEXTURE_2D, self.btn_buy_life_tex)
        self.draw_quad(300, 250, 200, 100)  #Botão centralizado

        #Desenha o botão de Sair/Restart abaixo
        glBindTexture(GL_TEXTURE_2D, self.btn_exit_tex)
        self.draw_quad(350, 150, 100, 50)

        glColor4f(1, 1, 1, 1)  #Reseta a cor para o padrão

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.background_texture)
        self.draw_quad(-self.camera_x * 0.2, 0, 8000, 600)

        glBindTexture(GL_TEXTURE_2D, self.solo_texture)
        for g in self.ground_segments: self.draw_quad(g.x - self.camera_x, g.y, g.w, g.h)

        glBindTexture(GL_TEXTURE_2D, self.platform_texture)
        for p in self.platforms: self.draw_quad(p.x - self.camera_x, p.y, p.w, p.h)

        self.finish_line.draw(self.camera_x)
        for c in self.coins: c.draw(self.camera_x)
        for e in self.enemies: e.draw(self.camera_x)

        #Desenho do Bafo no Cano
        for e2 in self.enemies2: e2.draw(self.camera_x)

        self.player.draw(self.camera_x)
    #Desenha um quadrado e cola uma textura nele
    def draw_quad(self, x, y, w, h):
        #glTexCoord2f: parte da imagem, define qual parte da textura será usada em cada vértice do objeto
        #glVertex2f: posição na tela
        #Isso serve porque o OpenGL precisa saber como mapear a imagem no objeto.
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