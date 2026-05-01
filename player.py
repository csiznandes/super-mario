import glfw
from OpenGL.GL import *
from texture import load_texture
from audio import AudioPulo
class Player:

    def __init__(self):

        self.x = 0
        self.y = 0

        self.w = 64
        self.h = 64

        self.vel_y = 0
        self.prev_y = self.y

        self.speed = 300
        self.gravity = 900
        self.jump_force = 480


        self.facing_right = True
        self.on_ground = False

        #Som
        self.som_pulo = AudioPulo()

        #Animação
        self.frames = [
            load_texture("assets/mickey/passo 1.png"),
            load_texture("assets/mickey/passo 2.png"),
            load_texture("assets/mickey/passo 3.png"),
            load_texture("assets/mickey/passo 4.png"),
            load_texture("assets/mickey/passo 5.png"),
            load_texture("assets/mickey/passo 6.png"),
            load_texture("assets/mickey/passo 7.png"),
            load_texture("assets/mickey/passo 8.png")
        ]

        self.frame_index = 0
        self.frame_time = 0
        self.frame_speed = 0.1


        self.current_texture = self.frames[0]

    def update(self, window, dt):
        self.prev_y = self.y

        moving = False

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.x -= self.speed * dt
            self.facing_right = False
            moving = True

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.x += self.speed * dt
            self.facing_right = True
            moving = True

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS and self.on_ground:
            self.som_pulo.tocar()
            self.vel_y = self.jump_force
            self.on_ground = False

        self.vel_y -= self.gravity * dt

        if moving:
            self.frame_time += dt

            if self.frame_time >= self.frame_speed:
                self.frame_time = 0
                self.frame_index += 1

                if self.frame_index >= len(self.frames):
                    self.frame_index = 0

                self.current_texture = self.frames[self.frame_index]
        else:
            self.frame_index = 0
            self.current_texture = self.frames[0]

    def draw(self, camera_x):
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