from typing import Tuple, Set, Iterable
from fractions import Fraction


POB = 11
KAVAL = 12
BABA = 13
KRALJ = 14

TAROK = "tarok"
PIK = "pik"
KRIZ = "kriz"
SRCE = "srce"
KARA = "kara"

SLIKICE = [POB, KAVAL, BABA, KRALJ]
imena_slik = {POB: "pob", KAVAL: "kaval", BABA: "baba", KRALJ: "kralj"}

BARVE = [PIK, KRIZ, SRCE, KARA]
karte_pomo = {(barva, slika) for barva in BARVE for slika in SLIKICE}  # type: Set[Tuple[str, int]]

# 1-9
rimske = [i * "I" for i in range(1, 5)] + ["V" + (i * "I") for i in range(4)]
rimske.append("IX")
# 10-13
rimske += ["X{}".format(i * "I") for i in range(4)]
# 14
rimske.append("XIV")
# 15-18
rimske += ["XV{}".format(i * "I") for i in range(4)]
# 19, 20, 21
rimske.append("XIX")
rimske.append("XX")
rimske.append("XXI")
rimske.append("skis")  # :)


class Karta:
    def __init__(self, barva: str, stevilcna_vrednost: int) -> None:
        assert (barva, stevilcna_vrednost) in karte_pomo
        self.barva = barva
        self.stevilcna_vrednost = stevilcna_vrednost
        # Se spomnimo? http://putka.upm.si/tasks/2011/2011_3kolo/tarok
        self.tockovna_vrednost = TOCKE[(self.barva, self.stevilcna_vrednost)] - Fraction(2, 3)
        self.ime = ""
        if self.barva == TAROK:
            self.ime = rimske[self.stevilcna_vrednost - 1]
        elif self.stevilcna_vrednost in SLIKICE:
            self.ime = imena_slik[self.stevilcna_vrednost]
        else:
            self.ime = str(self.stevilcna_vrednost)
        # za urejanje
        self.urejenost = 0
        if self.barva == TAROK:
            self.urejenost = self.stevilcna_vrednost + KRALJ  # da so vsi taroki > drugo
        elif self.tockovna_vrednost in SLIKICE or self.barva in [PIK, KRIZ]:
            self.urejenost = self.stevilcna_vrednost
        else:  # rdeci platelci
            self.urejenost = -self.stevilcna_vrednost

    def __repr__(self):
        if self.barva == TAROK:
            return self.ime
        else:
            return "{} {}".format(self.barva, self.ime)  # TODO: mogoc kej krajsega

    def __hash__(self):
        return (self.barva + str(self.stevilcna_vrednost)).__hash__()

    # Za primerjavo implementiram =, > in <, ker ni linearno urejeno ...

    def __eq__(self, other):
        return self.barva == other.barva and self.stevilcna_vrednost

    def __lt__(self, other):
        return self.barva == other.barva and self.urejenost < other.urejenost \
               or self.barva != TAROK and other.barva == TAROK

    def __gt__(self, other):
        return self.barva == other.barva and self.urejenost > other.urejenost \
               or self.barva == TAROK and other.barva != TAROK


def najvisja_karta(a: Iterable[Karta]):
    najvisja = None
    for k in a:
        if najvisja is None or k > najvisja:
            najvisja = k
    return najvisja


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

PALCKA = Karta(TAROK, 1)
MOND = Karta(TAROK, 21)
SKIS = Karta(TAROK, 22)
TRULA = {PALCKA, MOND, SKIS}


