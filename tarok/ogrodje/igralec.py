from random import shuffle, random

from typing import List, Set, Tuple, Iterable, Callable
from ogrodje.karte import Karta, TAROK, PALCKA, MOND, SKIS, najvisja_karta
from ogrodje.tipi import TipIgre, BERAC, ODPRTI_BERAC, KLOP


TALON_ID = 0


class Igralec:
    def __init__(self,
                 je_clovek: bool,
                 id_stevilka: int,
                 funkcija_poteze: 'Callable[[List[Igralec], List[List[Tuple[Igralec, Karta]]], List[Karta], int, Set[Karta], Set[Karta]], Karta]',
                 licitacijska_funkcija: 'Callable[[List[Igralec], List[Tuple[int, TipIgre]], int, Set[Karta], Set[TipIgre]], TipIgre]',
                 talon_izbiralka: Callable[[Set[Karta], List[List[Karta]]], List[Karta]],
                 talon_menjalka: Callable[[Set[Karta], List[Karta]], Set[Karta]]
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
        """
        Izracuna potezo.
        :param postavitev_igralcev: (ciklicni) seznam [igralec1_id, igralec2_id, ...], ki doloca vrstni red v igri
        :param dosedanje_licitiranje: seznam klicev do tega trenutka, kot so si sledili pri licitaciji
        :param dovoljene_igre: dopustni klici
        :return:
        """
        return self.licitacijska_funkcija(postavitev_igralcev, dosedanje_licitiranje, self.id, self.karte, dovoljene_igre)

    def dopustne_karte(self, delni_stih: List[Karta], igra: TipIgre) -> Set[Karta]:
        """
        Implementira pravila metanja kart na strani https://www.pagat.com/tarot/sltarok.html#play
        :param delni_stih:
        :param igra:
        :return:
        """
        # TODO: barvni valat

        if len(delni_stih) == 0:
            return self.karte

        barva_prve = delni_stih[0].barva

        # osnovni filter
        dovoljene = {karta for karta in self.karte if karta.barva == barva_prve}  # domo isto, ce jo mamo
        if len(dovoljene) == 0:
            if barva_prve == TAROK:  # ne mormo se odzvat s tarokom
                dovoljene = self.karte
            else:                    # ne mormo se odzvat z barvo
                dovoljene = {karta for karta in self.karte if karta.barva == TAROK}
                if len(dovoljene) == 0:  # nimamo niti tarokov
                    dovoljene = self.karte
        # posebne igre
        if igra in [KLOP, BERAC, ODPRTI_BERAC]:
            # ce je kaka dopustna (<--> vse dopustne) iste barve kot prva, dovolimo le visje ...
            # sicer: lahko damo karkoli

            # treba cez vse, ce se da
            max_stih = najvisja_karta(delni_stih)
            max_jaz = najvisja_karta(dovoljene)
            if max_jaz > max_stih:
                dovoljene = {karta for karta in dovoljene if karta > max_stih}

            # palica mora biti izsiljena, zato jo najprej vrzemo ven
            if PALCKA in dovoljene and len(dovoljene) > 1:
                dovoljene.remove(PALCKA)
            # in dodamo nazaj, ce
            # 1) je zadnja karta/(tarok in lahko igras taroke): za to poskrbljeno z 'and len(dovoljene) > 1'
            # 2) edina pobere stih
            if PALCKA in self.karte and SKIS in delni_stih and MOND in delni_stih:
                dovoljene.add(PALCKA)
        return dovoljene

    def odigraj_potezo(self,
                       postavitev_igralcev: 'List[Igralec]',
                       dosedanje_poteze: 'List[List[Tuple[Igralec, Karta]]]',
                       igra: TipIgre,
                       pobrano_iz_talona: List[Karta]
                       ) -> Karta:
        """
        Izracuna potezo.
        :param postavitev_igralcev: (ciklicni) seznam [igralec1_id, igralec2_id, ...], ki doloca vrstni red v igri
        :param dosedanje_poteze: seznam potez, vsaka poteza je casovno urejen (kot je potekala poteza) seznam parov
        (igralecID, Karta). Zadnja element predstavlja ze vrzene karte v dani potezi in je zato lahko krajsi kot tisti
        pred njim.
        :param igra:
        :param pobrano_iz_talona: karte, ki jih je aktivni igralec vzel iz talona
        :return: izbrana Karta
        """
        dovoljene = self.dopustne_karte([karta for (_, karta) in dosedanje_poteze[-1]], igra)
        izbrana = self.funkcija_poteze(postavitev_igralcev, dosedanje_poteze, pobrano_iz_talona, self.id, self.karte, dovoljene)
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
        return self.talon_izbiralka(self.karte, deli_talona)

    def zamenjaj_s_talonom(self, del_talona: List[Karta]) -> None:
        zalozeno = self.talon_menjalka(self.karte, del_talona)
        self.pobrano.append([])
        for karta in zalozeno:
            self.pobrano[-1].append(karta)
            self.karte.remove(karta)
