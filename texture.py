from OpenGL.GL import *
from PIL import Image #Manipula imagens

def load_texture(path):

    image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA") #Abre imagem, garante transparência e inverte verticalmente
    #Obs.: O sistema de coordenadas do OpenGL é invertido em relação ao padrão das imagens, por isso inverte verticalmente
    img_data = image.convert("RGBA").tobytes() #Transforma imagem em bytes, pois OpenGL somente entende bytes

    width, height = image.size

    texture = glGenTextures(1) #Gera ID da textura

    glBindTexture(GL_TEXTURE_2D, texture) #Ativa textura
    #Envia pra GPU
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
    glEnable(GL_BLEND) #Mistura de cores
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) #Define como transparência funciona
    #Filtros: suaviza imagem ao escalar
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture