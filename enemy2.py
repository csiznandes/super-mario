from OpenGL.GL import *
from texture import load_texture
from audio import AudioHitBafo

class Enemy2:
    def __init__(self, x, y):
        #Posição do cano
        self.pipe_x = x
        self.pipe_y = y
        self.pipe_w = 74
        self.pipe_h = 90

        #Inimigo
        self.w = 58
        self.h = 58
        self.x = self.pipe_x + (self.pipe_w / 2) - (self.w / 2)
        self.som_hit = AudioHitBafo()
        #Posição escondido e aparecendo
        self.hidden_y = self.pipe_y + 20
        self.out_y = self.pipe_y + self.pipe_h - 10
        self.y = self.hidden_y

        self.speed = 80
        self.direction = 1  # 1 = sobe, -1 = desce

        self.wait_timer = 0
        self.wait_time = 1.2
        #Carrega as texturas
        self.pipe_texture = load_texture("assets/enemy/cano.png")
        self.enemy_texture = load_texture("assets/enemy/bafo.png")

    def update(self, dt):
        self.wait_timer += dt
        #Espera antes de sair
        if self.wait_timer < self.wait_time:
            return
        #Movimento vertical
        self.y += self.speed * self.direction * dt

        if self.y >= self.out_y:
            self.y = self.out_y
            self.direction = -1
            self.wait_timer = 0

        elif self.y <= self.hidden_y:
            self.y = self.hidden_y
            self.direction = 1
            self.wait_timer = 0
    #Colisão com cano AABB
    def check_pipe_collision(self, player):
        colidiu = (
            player.x < self.pipe_x + self.pipe_w and
            player.x + player.w > self.pipe_x and
            player.y < self.pipe_y + self.pipe_h and
            player.y + player.h > self.pipe_y
        )

        if not colidiu:
            return

        #Player caindo em cima do cano
        if player.vel_y < 0 and player.y >= self.pipe_y + self.pipe_h - 10:
            player.y = self.pipe_y + self.pipe_h
            player.vel_y = 0
            player.on_ground = True
    #Colisão com inimigo
    def check_enemy_collision(self, player, game):
        #Só dá dano se o inimigo estiver saindo do cano
        if self.y <= self.hidden_y + 10:
            return

        colidiu = (
            player.x < self.x + self.w and
            player.x + player.w > self.x and
            player.y < self.y + self.h and
            player.y + player.h > self.y
        )

        if colidiu:
            game.lose_life()
            self.som_hit.tocar()

    def check_collision_with_player(self, player, game):
        self.check_pipe_collision(player)
        self.check_enemy_collision(player, game)

    def draw_quad(self, x, y, w, h, texture):
        glBindTexture(GL_TEXTURE_2D, texture)

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

    def draw(self, camera_x):
        screen_pipe_x = self.pipe_x - camera_x
        screen_enemy_x = self.x - camera_x

        #Desenha inimigo primeiro, para parecer que sai de dentro do cano
        self.draw_quad(
            screen_enemy_x,
            self.y,
            self.w,
            self.h,
            self.enemy_texture
        )

        #Desenha o cano por cima
        self.draw_quad(
            screen_pipe_x,
            self.pipe_y,
            self.pipe_w,
            self.pipe_h,
            self.pipe_texture
        )