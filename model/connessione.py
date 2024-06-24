from dataclasses import dataclass
@dataclass
class Connessione:
    v1:int
    v2:int
    t1:int
    t2:int


    def __str__(self):
        return f"{self.v1} - {self.v2}"