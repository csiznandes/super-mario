import winsound


### Classes de Audio do game para eventos ###


###################################
# falta classe para audio do game musica??#

class AudioPulo:


    def __init__(self):
        self.caminho = "assets/audio_pulo.wav"


    def tocar(self):
        winsound.PlaySound(
        self.caminho,
        winsound.SND_FILENAME | winsound.SND_ASYNC
        )


class AudioMusica:


    def __init__(self):
        self.caminho = "assets/mickeyfundo.wav"


    def tocar(self):
        winsound.PlaySound(
        self.caminho,
        winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
        )


class AudioHit:


    def __init__(self):
        self.caminho = "assets/audio_hit.wav"


    def tocar(self):
        winsound.PlaySound(
            self.caminho,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )



class AudioGamerover:


    def __init__(self):
        self.caminho = "assets/audio_gamerover.wav"


    def tocar(self):
        winsound.PlaySound(
        self.caminho,
        winsound.SND_FILENAME | winsound.SND_ASYNC
        )
