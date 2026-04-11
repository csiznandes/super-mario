class Platform:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_collision(self, player):

        player_bottom = player.y
        player_top = player.y + 64
        player_left = player.x
        player_right = player.x + 64

        platform_top = self.y + self.h
        platform_left = self.x
        platform_right = self.x + self.w

        if (
            player_right > platform_left and
            player_left < platform_right and
            player_bottom >= platform_top - 10 and
            player_bottom <= platform_top + 10 and
            player.vel_y <= 0
        ):
            player.y = platform_top
            player.vel_y = 0
            player.on_ground = True