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
KARTE_POMO = {(barva, slika) for barva in BARVE for slika in SLIKICE}

for i in range(len(BARVE)):
     obseg = range(7, 11) if i < 2 else range(1, 5)
     KARTE_POMO |= {(BARVE[i], platelc) for platelc in obseg}

BARVE.append(TAROK)
KARTE_POMO |= {(BARVE[-1], i) for i in range(1, 23)}
TOCKE = {}
for karta in KARTE_POMO:
    if karta[1] in SLIKICE:
        vred = SLIKICE.index(karta[1]) + 2
    elif karta[0] == TAROK and karta[1] in [1, 21, 22]:
        vred = 5
    else:
        vred = 1
    TOCKE[karta] = vred


class Karta:
    def __init__(self, barva, stevilcna_vrednost):
        assert (barva, stevilcna_vrednost) in KARTE_POMO
        self.barva = barva
        self.stevilcna_vrednost = stevilcna_vrednost
        self.tockovna_vrednost = TOCKE[(self.barva, self.stevilcna_vrednost)]

    def __repr__(self):
        return "Predstavitev karte za v tkinter"

KARTE = {Karta(barva, vred) for (barva, vred) in KARTE_POMO}

class OdlocitvenaFunckija:
    def __init__(self, funkcija):
        self.odlocitvena = funkcija

    def izracunaj(self, postavitev_igralcev, dosedanje_poteze, id_igralca, vse_karte_igralca, dovoljene_karte_igralca):
        """
        Izracuna potezo.
        :param postavitev_igralcev: (ciklicni) seznam [igralec1_id, igralec2_id, ...], ki doloca vrstni red v igri
        :param dosedanje_poteze: seznam potez, vsaka poteza je casovno urejen (kot je potekala poteza) seznam parov
        (igralecID, Karta). Zadnja element predstavlja ze vrzene karte v dani potezi in je zato lahko krajsi kot tisti
        pred njim.
        :param id_igralca:
        :param vse_karte_igralca: mnozica kart, ki jih ima igralec, katerega potezo je treba izracunati, v roki
        :param dovoljene_karte_igralca: dopustna podmnozica vse_karte_igralca, ki jih lahko vrze to potezo
        :return: izbrana Karta
        """
        return self.funkcija(postavitev_igralcev, dosedanje_poteze, id_igralca, vse_karte_igralca, dovoljene_karte_igralca)


class Igralec:
    def __init__(self, je_clovek, id_stevilka, odlocitvena_funkcija):
        """
        :param je_clovek: True ali False
        :param id_stevilka: id igralca
        :param odlocitvena_funkcija: ignoriramo if je_clovek else OdlocitvenaFunckija.
        :return:
        """
        self.cloveski = je_clovek
        self.id = id_stevilka
        self.odlocitvena_funkcija = odlocitvena_funkcija


class Tarok:
    def __init__(self, igralci):
        """
        :param igralci: seznam Igralcev
        :return:
        """
        self.igralci = igralci

    def odigraj(self):
        pass