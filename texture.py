from OpenGL.GL import *
from PIL import Image

def load_texture(path):

    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = image.convert("RGBA").tobytes()

    width, height = image.size

    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        width,
        height,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        img_data
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture