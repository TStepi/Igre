from random import shuffle, random

from typing import List, Set, Tuple, Iterable

from ogrodje.karte import Karta
from ogrodje.odlocanje.definicije.funkcija_poteze import FunkcijaPoteze
from ogrodje.odlocanje.definicije.licitacijska_funkcija import LicitacijskaFunkcija
from ogrodje.odlocanje.definicije.talonski_funkciji import IzbiralkaIzTalona, MenjalkaSTalonom
from ogrodje.tipi import TipIgre


class Igralec:
    def __init__(self,
                 je_clovek: bool,
                 id_stevilka: int,
                 funkcija_poteze: FunkcijaPoteze,
                 licitacijska_funkcija: LicitacijskaFunkcija,
                 talon_izbiralka: IzbiralkaIzTalona,
                 talon_menjalka: MenjalkaSTalonom
                 ) -> None:
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
        self.talon_izbiralka = talon_izbiralka
        self.talon_menjalka = talon_menjalka
        self.karte = set()  # type: Set[Karta]
        self.pobrano = []  # type: List[List[Karta]]
        self.st_pobranih_stihov = 0

    def __eq__(self, other):
        return self.id == other.id

    def poberi_dodeljene_karte(self, karte: Iterable[Karta]) -> None:
        """
        Shranimo mnozico Kart v self.karte
        :param karte: mnozica dodeljenih Kart
        :return:
        """
        for karta in karte:
            self.karte.add(karta)

    def poberi_stih(self, karte: Iterable[Karta]) -> None:
        self.st_pobranih_stihov += 1
        self.pobrano.append([])
        for karta in karte:
            self.pobrano[-1].append(karta)

    def licitiraj(self,
                  postavitev_igralcev: 'List[Igralec]',
                  dosedanje_licitiranje: List[Tuple[int, TipIgre]],
                  dovoljene_igre: Set[TipIgre]
                  ) -> TipIgre:
        return self.licitacijska_funkcija.izracunaj(postavitev_igralcev, dosedanje_licitiranje, self.id, self.karte, dovoljene_igre)

    def dopustne_karte(self, seznam_odvrzenih: List[Karta]) -> Set[Karta]:
        raise Exception("hihi")

    def odigraj_potezo(self,
                       postavitev_igralcev: 'List[Igralec]',
                       dosedanje_poteze: 'List[List[Tuple[Igralec, Karta]]]'
                       ) -> Karta:
        dovoljene = self.dopustne_karte([karta for (_, karta) in dosedanje_poteze[-1]])
        izbrana = self.funkcija_poteze.izracunaj(postavitev_igralcev, dosedanje_poteze, self.id, self.karte, dovoljene)
        self.karte.remove(izbrana)
        return izbrana

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
                igralci[i].poberi_dodeljene_karte(paketek)
                ind += kolko
        return talon

    def izberi_iz_talona(self, deli_talona: List[List[Karta]]) -> List[Karta]:
        return self.talon_izbiralka.izracunaj(self.karte, deli_talona)

    def zamenjaj_s_talonom(self, del_talona: List[Karta]) -> None:
        zalozeno = self.talon_menjalka.izracunaj(self.karte, del_talona)
        self.pobrano.append([])
        for karta in zalozeno:
            self.pobrano[-1].append(karta)
            self.karte.remove(karta)
