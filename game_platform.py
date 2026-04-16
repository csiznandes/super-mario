class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_collision(self, player):
        if (
            player.x + player.w <= self.x or
            player.x >= self.x + self.w or
            player.y > self.y + self.h or
            player.y < self.y or
            player.vel_y > 0
        ):
            return

        player.y = self.y + self.h
        player.vel_y = 0
        player.on_ground = True