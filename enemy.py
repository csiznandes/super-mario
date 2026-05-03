from OpenGL.GL import *
from texture import load_texture
from audio import AudioHitEnemy
#Inimigo que anda
class Enemy:
    def __init__(self, platform):
        #Tamanho
        self.w = 32
        self.h = 32
        #Fica somente em cima da plataforma
        self.y = platform.y + platform.h
        self.x = platform.x + (platform.w / 2) - (self.w / 2)
        self.min_x = platform.x
        self.max_x = platform.x + platform.w - self.w
        #Outras configurações
        self.speed = 100
        self.direction = 1
        self.facing_right = True
        self.ativo = True
        self.dead_timer = 0
        self.remove = False
        self.son_hit = AudioHitEnemy()
        #Animação dos passos
        self.frames = [
            load_texture("assets/enemy/passo1.png"),
            load_texture("assets/enemy/passo2.png"),
            load_texture("assets/enemy/passo3.png"),
            load_texture("assets/enemy/passo4.png"),
            load_texture("assets/enemy/passo5.png"),
            load_texture("assets/enemy/passo6.png"),
        ]

        self.hit_texture = load_texture("assets/enemy/hit.png")

        self.frame_index = 0
        self.frame_time = 0
        self.frame_speed = 0.12
        self.current_texture = self.frames[0]

    def update(self, dt):
        if not self.ativo:
            self.current_texture = self.hit_texture
            self.dead_timer += dt #Tempo até desaparecer

            if self.dead_timer >= 0.3:
                self.remove = True
            return
        #Movimento com delta time
        self.x += self.speed * self.direction * dt

        if self.x >= self.max_x:
            self.x = self.max_x
            self.direction = -1
            self.facing_right = False

        elif self.x <= self.min_x:
            self.x = self.min_x
            self.direction = 1
            self.facing_right = True

        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.current_texture = self.frames[self.frame_index]
    #Colisão com jogador AABB. Se jogador caiu por cima, mata inimigo e faz jogador quicar. Se não, jogador toma dano
    def check_collision_with_player(self, player, game):
        if not self.ativo:
            return

        colidiu = (
            player.x < self.x + self.w and
            player.x + player.w > self.x and
            player.y < self.y + self.h and
            player.y + player.h > self.y
        )

        if not colidiu:
            return

        if player.vel_y < 0 and player.y > self.y + (self.h * 0.5):
            self.die()
            player.vel_y = player.jump_force * 0.8
            player.on_ground = False
        else:
            game.lose_life()
    #Desativar inimigo
    def die(self):
        self.ativo = False
        self.current_texture = self.hit_texture
        self.dead_timer = 0
        self.son_hit.tocar()

    def draw(self, camera_x):
        if self.remove:
            return

        glBindTexture(GL_TEXTURE_2D, self.current_texture)

        screen_x = self.x - camera_x

        glBegin(GL_QUADS)

        if self.facing_right:
            glTexCoord2f(0, 0)
            glVertex2f(screen_x, self.y)

            glTexCoord2f(1, 0)
            glVertex2f(screen_x + self.w, self.y)

            glTexCoord2f(1, 1)
            glVertex2f(screen_x + self.w, self.y + self.h)

            glTexCoord2f(0, 1)
            glVertex2f(screen_x, self.y + self.h)
        else:
            glTexCoord2f(1, 0)
            glVertex2f(screen_x, self.y)

            glTexCoord2f(0, 0)
            glVertex2f(screen_x + self.w, self.y)

            glTexCoord2f(0, 1)
            glVertex2f(screen_x + self.w, self.y + self.h)

            glTexCoord2f(1, 1)
            glVertex2f(screen_x, self.y + self.h)

        glEnd()