from typing import Tuple, Set, Any
from fractions import Fraction

class Karta:
    def __init__(self, barva: str, stevilcna_vrednost) -> None:
        assert (barva, stevilcna_vrednost) in karte_pomo
        self.barva = barva
        self.stevilcna_vrednost = stevilcna_vrednost
        # Se spomnimo? http://putka.upm.si/tasks/2011/2011_3kolo/tarok
        self.tockovna_vrednost = TOCKE[(self.barva, self.stevilcna_vrednost)] - Fraction(2, 3)

    def __repr__(self):
        return "Predstavitev karte za v tkinter"


POB = "pob"
KAVAL = "kaval"
BABA = "baba"
KRALJ = "kralj"
TAROK = "tarok"
PIK = "pik"
KRIZ = "kriz"
SRCE = "srce"
KARA = "kara"

SLIKICE = [POB, KAVAL, BABA, KRALJ]
BARVE = [PIK, KRIZ, SRCE, KARA]
karte_pomo = {(barva, slika) for barva in BARVE for slika in SLIKICE}  # type: Set[Tuple[str, Any]]

for i in range(len(BARVE)):
    obseg = range(7, 11) if i < 2 else range(1, 5)
    karte_pomo |= {(BARVE[i], platelc) for platelc in obseg}

BARVE.append(TAROK)
karte_pomo |= {(BARVE[-1], i) for i in range(1, 23)}
TOCKE = {}
trula_vrednosti = [1, 21, 22]
for karta in karte_pomo:
    if karta[1] in SLIKICE:
        vred = SLIKICE.index(karta[1]) + 2
    elif karta[0] == TAROK and karta[1] in trula_vrednosti:
        vred = 5
    else:
        vred = 1
    TOCKE[karta] = vred

KARTE = {Karta(barva, vred) for (barva, vred) in karte_pomo}  # type: Set[Karta]
KRALJI = {Karta(barva, KRALJ) for barva in BARVE if barva != TAROK}
TRULA = {Karta(TAROK, i) for i in trula_vrednosti}
PALCKA = Karta(TAROK, 1)
