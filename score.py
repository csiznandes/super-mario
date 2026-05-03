from OpenGL.GL import *
from texture import load_texture


class Score:
    def __init__(self, width, height):
        self.score = 0
        self.width = width
        self.height = height

        #carregar números
        self.number_textures = {
            "0": load_texture("assets/numbers/number0.png"),
            "1": load_texture("assets/numbers/number1.png"),
            "2": load_texture("assets/numbers/number2.png"),
            "3": load_texture("assets/numbers/number3.png"),
            "4": load_texture("assets/numbers/number4.png"),
            "5": load_texture("assets/numbers/number5.png"),
            "6": load_texture("assets/numbers/number6.png"),
            "7": load_texture("assets/numbers/number7.png"),
            "8": load_texture("assets/numbers/number8.png"),
            "9": load_texture("assets/numbers/number9.png"),
        }

    def add(self, value):
        self.score += value

    def reset(self):
        self.score = 0

    def draw(self):
        score_text = str(self.score)

        digit_w = 24
        digit_h = 32
        spacing = 4

        total_w = len(score_text) * digit_w + (len(score_text) - 1) * spacing

        start_x = self.width - total_w - 20
        start_y = self.height - 50

        glColor3f(1, 1, 1)

        for i, digit in enumerate(score_text):
            texture = self.number_textures[digit]

            x = start_x + i * (digit_w + spacing)
            y = start_y

            glBindTexture(GL_TEXTURE_2D, texture)

            glBegin(GL_QUADS)

            glTexCoord2f(0, 0)
            glVertex2f(x, y)

            glTexCoord2f(1, 0)
            glVertex2f(x + digit_w, y)

            glTexCoord2f(1, 1)
            glVertex2f(x + digit_w, y + digit_h)

            glTexCoord2f(0, 1)
            glVertex2f(x, y + digit_h)

            glEnd()