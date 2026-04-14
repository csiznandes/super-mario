import winsound

class AudioPulo:
    def __init__(self):
        self.caminho = "assets/audio_pulo.wav"

    def tocar(self):
        winsound.PlaySound(self.caminho, winsound.SND_FILENAME | winsound.SND_ASYNC)

#classe para audio do game musica

#classe audio_musica

#classe audio_hit


#classe audio_gamerover
