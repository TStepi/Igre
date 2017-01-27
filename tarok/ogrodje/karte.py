class Karta:
    def __init__(self, barva, stevilcna_vrednost):
        assert (barva, stevilcna_vrednost) in karte_pomo
        self.barva = barva
        self.stevilcna_vrednost = stevilcna_vrednost
        self.tockovna_vrednost = TOCKE[(self.barva, self.stevilcna_vrednost)]

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
karte_pomo = {(barva, slika) for barva in BARVE for slika in SLIKICE}

for i in range(len(BARVE)):
    obseg = range(7, 11) if i < 2 else range(1, 5)
    karte_pomo |= {(BARVE[i], platelc) for platelc in obseg}

BARVE.append(TAROK)
karte_pomo |= {(BARVE[-1], i) for i in range(1, 23)}
TOCKE = {}
for karta in karte_pomo:
    if karta[1] in SLIKICE:
        vred = SLIKICE.index(karta[1]) + 2
    elif karta[0] == TAROK and karta[1] in [1, 21, 22]:
        vred = 5
    else:
        vred = 1
    TOCKE[karta] = vred

KARTE = {Karta(barva, vred) for (barva, vred) in karte_pomo}