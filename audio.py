import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class AudioManager:
    iniciado = False

    @classmethod
    def iniciar(cls):
        if not cls.iniciado:
            pygame.mixer.init()
            cls.iniciado = True


class AudioPulo:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_pulo.WAV")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()


class AudioHitEnemy:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_hit_anemy.WAV")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()


class AudioHitMickey:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_hit_mickey.WAV")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()


class AudioMusica:
    def __init__(self):
        AudioManager.iniciar()
        self.caminho = os.path.join(BASE_DIR, "assets", "audio", "mickeyfundo.wav")

    def tocar(self):
        pygame.mixer.music.load(self.caminho)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def parar(self):
        pygame.mixer.music.stop()

    def pausar(self):
        pygame.mixer.music.pause()

    def continuar_(self):
        pygame.mixer.music.unpause()