from dataclasses import dataclass

@dataclass
class Connessione:
    _id_rifugio1 : int
    _id_rifugio2 : int
    _distanza : float
    _difficolta : str
    _anno :int

    def __str__(self):
        return f"{self._id_rifugio1} {self._id_rifugio2} {self._distanza} {self._difficolta} {self._anno}"

    def __hash__(self):
        return hash(self._id_rifugio1), hash(self._id_rifugio2)