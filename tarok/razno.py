SLIKICE = ["pob", "kaval", "baba", "kralj"]
BARVE = ["pik", "kriz", "srce", "kara"]
KARTE = {(barva, slika) for barva in BARVE for slika in SLIKICE}

for i in range(len(BARVE)):
     obseg = range(7, 11) if i < 2 else range(1, 5)
     KARTE |= {(BARVE[i], platelc) for platelc in obseg}

BARVE.append("tarok")
KARTE |= {(BARVE[-1], i) for i in range(1, 23)} # skisa nisem dal posebi, ker je lazi primerjat, lahko pa se hecamo
                                                # Karta.__ge__ itd, ce bo treba met kompleksne primerjave


class Karta:
    def __init__(self, barva, vrednost):
        assert (barva, vrednost) in KARTE
        self.barva = barva
        self.vrednost = vrednost

    def __repr__(self):
        return "Predstavitev karte za v tkinter"


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
    def __init__(self, je_clovek, odlocitvena_funkcija):
        """
        :param je_clovek: True ali False
        :param odlocitvena_funkcija: ignoriramo if je_clovek else OdlocitvenaFunckija.
        :return:
        """
        self.cloveski = je_clovek
        self.odlocitvena_funkcija = odlocitvena_funkcija


class Tarok:
    def __init__(self, igralci):
        """
        :param igralci: seznam Igralcev
        :return:
        """
        self.igralci = igralci

    def __odigraj__(self):
        pass