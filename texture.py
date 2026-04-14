from OpenGL.GL import *
from PIL import Image
#import numpy as np

def load_texture(path):

    #image = Image.open(path)
    #image = image.transpose(Image.FLIP_TOP_BOTTOM)

    image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    #image_data = np.array(image).flatten()

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
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture