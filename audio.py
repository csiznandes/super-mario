import os #Manipular caminhos de arquivos
import pygame #Usado para o som, conforme autorizado pelo professor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #Garantir que os arquivos de áudio funcionem em qualquer máquina
#Controle global do áudio
class AudioManager:
    iniciado = False

    @classmethod
    def iniciar(cls):
        if not cls.iniciado: #Só inicializa o áudio uma vez, para evitar erro de reinicialização do mixer
            pygame.mixer.init()
            cls.iniciado = True
#Áudio do pulo
class AudioPulo:
    def __init__(self):
        AudioManager.iniciar() #Garante que o áudio está pronto antes de usar
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_pulo.WAV")
        self.som = pygame.mixer.Sound(caminho)
    #Toca o som
    def tocar(self):
        self.som.play()
#Áudio de dano do inimigo 1 - mesmo modo de funcionamento do áudio do pulo
class AudioHitEnemy:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_hit_anemy.WAV")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()
#Áudio de dano do inimigo 2 - mesmo modo de funcionamento do áudio do pulo
class AudioHitBafo:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_hit_bafo.wav")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()
#Áudio de dano do Mickey - mesmo modo de funcionamento do áudio do pulo
class AudioHitMickey:
    def __init__(self):
        AudioManager.iniciar()
        caminho = os.path.join(BASE_DIR, "assets", "audio", "audio_hit_mickey.WAV")
        self.som = pygame.mixer.Sound(caminho)

    def tocar(self):
        self.som.play()
#Música de fundo
class AudioMusica:
    def __init__(self):
        AudioManager.iniciar()
        self.caminho = os.path.join(BASE_DIR, "assets", "audio", "mickeyfundo.wav")
    #Toca a música, mas não carrega tudo na memória
    def tocar(self):
        pygame.mixer.music.load(self.caminho)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1) #Loop infinito da música
    #Controles básicos de música
    def parar(self):
        pygame.mixer.music.stop()

    def pausar(self):
        pygame.mixer.music.pause()

    def continuar_(self):
        pygame.mixer.music.unpause()