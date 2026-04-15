class Platform:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def check_collision(self, player):
        if player.x + player.w <= self.x or player.x >= self.x + self.w or player.y > self.y + self.h or player.y < self.y or player.vel_y > 0:
            return
        # exemplo simples de colisão por cima
        player.y = self.y + self.h
        player.vel_y = 0
        player.on_ground = True

        class Muro:
            def __init__(self, config, x_poss, textura):
                self.ultrapassado = False
                self.config = config
                self.xpos = x_poss
                self.largura = config["MURO_LARGURA"]
                self.gap = config["GAP"]
                self.velocidade = config["MURO_SPEED"]
                self.textura = textura
                self.reset()