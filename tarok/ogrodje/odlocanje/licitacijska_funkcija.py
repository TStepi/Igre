class LicitacijskaFunkcija:
    def __init__(self, funkcija):
        self.funkcija = funkcija

    def izracunaj(self, postavitev_igralcev, dosedanji_klici, id_igralca, karte_igralca):
        """
        Izracuna potezo.
        :param postavitev_igralcev: (ciklicni) seznam [igralec1_id, igralec2_id, ...], ki doloca vrstni red v igri
        :param dosedanji_klici: seznam klicev do tega trenutka, kot so si sledili pri licitaciji
        :param id_igralca: id_igralca, ki je na vrsti
        :param karte_igralca: mnozica Kart, ki jih ima igralec v rokah
        :return:
        """
        return self.funkcija(postavitev_igralcev, dosedanji_klici, id_igralca, karte_igralca)
