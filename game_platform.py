class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_collision(self, player):
        # colisão horizontal
        if player.x + player.w <= self.x or player.x >= self.x + self.w:
            return

        topo = self.y + self.h

        # só quando está caindo
        if player.vel_y <= 0:
            # verifica se cruzou o topo vindo de cima
            if player.prev_y >= topo and player.y <= topo:
                player.y = topo
                player.vel_y = 0
                player.on_ground = True