from ogrodje.igralec import Igralec
from ogrodje.karte import KARTE
from typing import List, Tuple

from ogrodje.tipi import TipIgre, IGRE, KLOP


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

    def licitacija(self) -> None:
        aktivni_licitatorji = self.igralci[2:] + self.igralci[:2]
        s_prednostjo = aktivni_licitatorji[-1]
        najvisja = IGRE[KLOP]  # type: TipIgre
        seznam_licitacij = []  # type: List[Tuple[int, TipIgre]]
        while len(aktivni_licitatorji) > 0:
            pomo = []
            for igralec in aktivni_licitatorji:
                na_izbiro = {igra for ime, igra in IGRE.items() if igra == KLOP or
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
        for runda in range(rund):
            pass

    def prestej_tocke(self, igralec: Igralec) -> int:
        return 70

    def odigraj_igro(self):
        kupcek = [karta for karta in KARTE]
        self.mesalec.premesaj(kupcek)
        self.privzigovalec.privzdigni(kupcek)

        talon = self.mesalec.razdeli(kupcek, self.igralci)  # po tem trenutku imajo vsi igralci svoje karte

        self.licitacija()

        self.odigraj_runde()
