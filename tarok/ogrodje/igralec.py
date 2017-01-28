from ogrodje.odlocanje.licitacijska_funkcija import LicitacijskaFunkcija
from ogrodje.odlocanje.funkcija_poteze import FunkcijaPoteze
from random import shuffle, random
from typing import List, Set
from ogrodje.karte import Karta
from ogrodje.tipi import TipIgre


class Igralec:
    def __init__(self,
                 je_clovek: bool,
                 id_stevilka: int,
                 funkcija_poteze: FunkcijaPoteze,
                 licitacijska_funkcija: LicitacijskaFunkcija) -> None:
        """
        :param je_clovek: True ali False
        :param id_stevilka: id igralca
        :param funkcija_poteze: ignoriramo if je_clovek else OdlocitvenaFunckija.
        :return:
        """
        self.cloveski = je_clovek
        self.id = id_stevilka
        self.funkcija_poteze = funkcija_poteze
        self.licitacijska_funkcija = licitacijska_funkcija
        self.karte = set()  # type: Set[Karta]
        self.pobrano = set()  # type: Set[Karta]

    def dvigni_karte_z_mize(self, karte: Set[Karta]) -> None:
        """
        Shranimo mnozico Kart v self.karte
        :param karte: mnozica dodeljenih Kart
        :return:
        """
        self.karte |= karte

    def licitiraj(self,
                  postavitev_igralcev: 'List[Igralec]',
                  dosedanje_licitiranje: List[TipIgre],
                  dovoljene_igre: Set[TipIgre]) -> TipIgre:
        return self.licitacijska_funkcija.izracunaj(postavitev_igralcev, dosedanje_licitiranje, self.id, self.karte, dovoljene_igre)

    def dopustne_karte(self, seznam_odvrzenih: List[Karta]) -> Set[Karta]:
        raise Exception("hihi")

    def odigraj_potezo(self, postavitev_igralcev, dosedanje_poteze):
        dovoljene = self.dopustne_karte(dosedanje_poteze[-1])
        return self.funkcija_poteze.izracunaj(postavitev_igralcev, dosedanje_poteze, self.id, self.karte, dovoljene)

    def premesaj(self, kup_kart: List[Karta]) -> None:
        shuffle(kup_kart)

    def privzdigni(self, kup_kart: List[Karta]) -> List[Karta]:
        i = int(random() * len(kup_kart))
        return kup_kart[i:] + kup_kart[:i]

    def razdeli(self, sez_kart: List[Karta], igralci: 'List[Igralec]') -> List[Karta]:
        talon = sez_kart[:6]
        st_igralcev = len(igralci)
        ind = 6
        stevilo_kart = (len(sez_kart) - 6) // st_igralcev
        # proper deljenje
        st_krogov = 2
        for krog in range(st_krogov):
            for i in range(st_igralcev):
                kolko = stevilo_kart // st_krogov
                paketek = {sez_kart[ind + j] for j in range(kolko)}
                igralci[i].dvigni_karte_z_mize(paketek)
                ind += kolko
        return talon
