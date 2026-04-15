import winsound
import os

class AudioPulo:
    def __init__(self):
        self.caminho = "assets/audio_pulo.wav"

    def tocar(self):
        if os.path.exists(self.caminho):
            winsound.PlaySound(
                self.caminho,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        else:
            print("Arquivo de áudio não encontrado:", self.caminho)
#classe para audio do game musica

#classe audio_musica

#classe audio_hit


#classe audio_gamerover
