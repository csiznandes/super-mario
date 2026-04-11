import glfw

class Player:

    def __init__(self):

        self.x = 100
        self.y = 100

        self.vel_y = 0

        self.speed = 300
        self.gravity = 900
        self.jump_force = 450

        self.on_ground = False

    def update(self, window, dt):

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.x -= self.speed * dt

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.x += self.speed * dt

        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

        self.vel_y -= self.gravity * dt
        self.y += self.vel_y * dt

        if self.y <= 100:
            self.y = 100
            self.vel_y = 0
            self.on_ground = True