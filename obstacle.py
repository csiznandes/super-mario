class Obstacle:
    def __init__(self, x, y, w, h):
        #Posição e tamanho
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    #Colisão, mas contrária à AABB
    def check_collision(self, player, game):
        if (
            player.x + player.w < self.x or
            player.x > self.x + self.w or
            player.y + player.h < self.y or
            player.y > self.y + self.h
        ):
            return

        #Jogador encostou: perde vida
        game.lose_life()

    def draw(self, camera_x, texture, draw_quad):
        draw_quad(self.x - camera_x, self.y, self.w, self.h)