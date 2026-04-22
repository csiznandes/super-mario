from OpenGL.GL import *
from texture import load_texture


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.w = 24
        self.h = 24

        self.collected = False
        self.value = 5

        self.frames = [
            load_texture("assets/coin/coin1.png"),
            load_texture("assets/coin/coin2.png"),
            load_texture("assets/coin/coin3.png"),
            load_texture("assets/coin/coin4.png"),
        ]

        self.frame_index = 0
        self.frame_time = 0
        self.frame_speed = 0.12
        self.current_texture = self.frames[0]

    def update(self, dt):
        if self.collected:
            return

        self.frame_time += dt

        if self.frame_time >= self.frame_speed:
            self.frame_time = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.current_texture = self.frames[self.frame_index]

    def check_collision_with_player(self, player):
        if self.collected:
            return 0

        colidiu = (
            player.x < self.x + self.w and
            player.x + player.w > self.x and
            player.y < self.y + self.h and
            player.y + player.h > self.y
        )

        if colidiu:
            self.collected = True
            return self.value

        return 0

    def draw(self, camera_x):
        if self.collected:
            return

        screen_x = self.x - camera_x

        glBindTexture(GL_TEXTURE_2D, self.current_texture)
        glColor3f(1, 1, 1)

        glBegin(GL_QUADS)

        glTexCoord2f(0, 0)
        glVertex2f(screen_x, self.y)

        glTexCoord2f(1, 0)
        glVertex2f(screen_x + self.w, self.y)

        glTexCoord2f(1, 1)
        glVertex2f(screen_x + self.w, self.y + self.h)

        glTexCoord2f(0, 1)
        glVertex2f(screen_x, self.y + self.h)

        glEnd()