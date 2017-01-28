from typing import List, Tuple, Set, Callable
from ogrodje.igralec import Igralec
from ogrodje.karte import Karta


class FunkcijaPoteze:
    def __init__(self,
                 funkcija: Callable[[List[Igralec], List[List[Tuple[Igralec, Karta]]], int, Set[Karta], Set[Karta]], Karta]
                 ) -> None:
        self.funkcija = funkcija

    def izracunaj(self,
                  postavitev_igralcev: List[Igralec],
                  dosedanje_poteze: List[List[Tuple[Igralec, Karta]]],
                  id_igralca: int,
                  vse_karte_igralca: Set[Karta],
                  dovoljene_karte_igralca: Set[Karta]
                  ) -> Karta:
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