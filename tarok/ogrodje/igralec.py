from random import shuffle, random

from typing import List, Set, Tuple, Iterable

from ogrodje.karte import Karta, TAROK, PALCKA
from ogrodje.odlocanje.definicije.funkcija_poteze import FunkcijaPoteze
from ogrodje.odlocanje.definicije.licitacijska_funkcija import LicitacijskaFunkcija
from ogrodje.odlocanje.definicije.talonski_funkciji import IzbiralkaIzTalona, MenjalkaSTalonom
from ogrodje.tarok import TALON_ID
from ogrodje.tipi import TipIgre, BERAC, KLOP


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
        assert self.id != TALON_ID
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

    def dopustne_karte(self, delni_stih: List[Karta], igra: TipIgre) -> Set[Karta]:
        if len(delni_stih) == 0:
            return self.karte

        barva_prve = delni_stih[0].barva

        # TODO: poskrbi tu za pravila s trulo
        # if dva od trule al neki:
        #     vrni tretjega od trule

        # osnovni filter
        dovoljene = {karta for karta in self.karte if karta.barva == barva_prve}
        if len(dovoljene) == 0:
            # nimamo iste barve
            if barva_prve == TAROK:
                dovoljene = self.karte  # nimamo taroka --> karkoli
            else:
                dovoljene = {karta for karta in self.karte if karta.barva == TAROK}  # skrti smo barve
                if len(dovoljene) == 0:  # zal tudi tarokov
                    dovoljene = self.karte
        # dopolnilna
        if igra in [KLOP, BERAC]:
            # ce je kaka dopustna (<--> vse dopustne) iste barve kot prva, dovolimo le visje ...
            # sicer: lahko damo karkoli
            for neka_nasa in dovoljene:
                break  # tako najhitreje do neke karte
            if neka_nasa.barva == barva_prve:
                najvecja = delni_stih[0]
                for karta in delni_stih[1:]:
                    if karta.barva == barva_prve and karta > najvecja:
                        najvecja = karta
                dovoljene = {k for k in dovoljene if k > najvecja}
            else:
                pass
            # palica mora biti izsiljena, a teh if-ov nau konc al kaj
            if PALCKA in dovoljene:
                if len(dovoljene) > 1:
                    dovoljene.remove(PALCKA)
        return dovoljene

    def odigraj_potezo(self,
                       postavitev_igralcev: 'List[Igralec]',
                       dosedanje_poteze: 'List[List[Tuple[Igralec, Karta]]]',
                       igra: TipIgre,
                       pobrano_iz_talona: List[Karta]
                       ) -> Karta:
        dovoljene = self.dopustne_karte([karta for (_, karta) in dosedanje_poteze[-1]], igra)
        izbrana = self.funkcija_poteze.izracunaj(postavitev_igralcev, dosedanje_poteze, pobrano_iz_talona, self.id, self.karte, dovoljene)
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
