from ogrodje.igralec import Igralec
from ogrodje.karte import KARTE
from typing import List, Tuple

from ogrodje.karte import Karta
from ogrodje.tipi import TipIgre, IGRE, KLOP, BERAC, ODPRTI_BERAC, SOLO_BREZ


class Tarok:
    def __init__(self, igralci: List[Igralec]) -> None:
        """
        :param igralci: seznam igralcev: prvi mesa, potem pa v smeri urinega kazalca
        :return:
        """
        assert len(igralci) == 3
        self.igralci = igralci
        self.mesalec = self.igralci[0]
        self.privzigovalec = self.igralci[2]  # ok za 3 in 4 igralce

        self.tocke = {}  # type: Dict[Igralec, int]

    def licitacija(self) -> None:
        aktivni_licitatorji = self.igralci[2:] + self.igralci[:2]
        s_prednostjo = aktivni_licitatorji[-1]
        najvisja = KLOP  # type: TipIgre
        seznam_licitacij = []  # type: List[Tuple[int, TipIgre]]
        while len(aktivni_licitatorji) > 0:
            pomo = []
            for igralec in aktivni_licitatorji:
                na_izbiro = {igra for igra in IGRE if igra == KLOP or
                                                      igra > najvisja or
                                                      igra == najvisja and igralec == s_prednostjo}
                igra = igralec.licitiraj(self.igralci, seznam_licitacij, na_izbiro)
                seznam_licitacij.append((igralec.id, igra))
                if igra.ime != KLOP:
                    pomo.append(igralec)
                else:
                    self.aktivni_igralec = igralec
                    najvisja = igra
            aktivni_licitatorji = [igralec for igralec in pomo]

        self.tip_igre = najvisja

    def odigraj_runde(self) -> None:
        rund = len(self.aktivni_igralec.karte)
        prvi = 1
        if self.tip_igre in {BERAC, ODPRTI_BERAC, SOLO_BREZ}:
            prvi = self.igralci.index(self.aktivni_igralec)
        n = len(self.igralci)
        poteze = []  # type: List[List[Tuple[Igralec, Karta]]]
        for runda in range(rund):
            poteze.append([])
            for j in range(n):
                igralec = self.igralci[(prvi + j) % n]
                karta = igralec.odigraj_potezo(self.igralci, poteze)
                poteze[-1].append((igralec, karta))
            zmagovalec_stiha = self.kdo_je_pobral(poteze[-1])
            zmagovalec_stiha.poberi_stih([karta for _, karta in poteze[-1]])

    def kdo_je_pobral(self, stih: List[Tuple[Igralec, Karta]]):
        return stih[0][0]

    def prestej_tocke(self) -> None:
        for igralec in self.igralci:
            vsota = 0
            for karta in igralec.pobrano:
                vsota += karta.tockovna_vrednost
            self.tocke[igralec] = round(vsota)

    def odigraj_igro(self):
        kupcek = [karta for karta in KARTE]
        self.mesalec.premesaj(kupcek)
        self.privzigovalec.privzdigni(kupcek)

        talon = self.mesalec.razdeli(kupcek, self.igralci)  # po tem trenutku imajo vsi igralci svoje karte

        self.licitacija()

        self.odigraj_runde()

        self.prestej_tocke()