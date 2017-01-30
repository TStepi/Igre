from typing import List, Tuple

from ogrodje.bonus import BONUSI, BONUS_PAGAT_ULTIMO
from ogrodje.igralec import Igralec
from ogrodje.karte import KARTE, Karta
from ogrodje.tipi import IGRE, KLOP, BERAC, ODPRTI_BERAC, SOLO_BREZ, TipIgre

VSE_TOCKE = 70
TALON_ID = 0


class Tarok:
    def __init__(self, igralci: List[Igralec]) -> None:
        """
        :param igralci: seznam igralcev: prvi mesa, potem pa v smeri urinega kazalca
        :return:
        """
        assert len(igralci) == 3
        self.igralci = igralci
        assert len({igralec.id for igralec in self.igralci}) == len(self.igralci)  # razlicni id-ji

        self.mesalec = self.igralci[0]
        self.aktivni_igralec = self.igralci[1]  # ta po defaultu zacne
        self.privzigovalec = self.igralci[2]  # ok za 3 in 4 igralce
        self.talon = []              # type: List[Karta]
        self.pobrano_iz_talona = []  # type: List[Karta]
        self.tip_igre = KLOP         # type: TipIgre
        self.tocke = {}              # type: Dict[Igralec, int]
        self.st_rund = (len(KARTE) - 6) // len(self.igralci)

    def licitacija(self) -> None:
        aktivni_licitatorji = self.igralci[2:] + self.igralci[:2]
        s_prednostjo = aktivni_licitatorji[-1]
        seznam_licitacij = []  # type: List[Tuple[int, TipIgre]]
        while len(aktivni_licitatorji) > 0:
            pomo = []
            for igralec in aktivni_licitatorji:
                na_izbiro = {igra for igra in IGRE if igra == KLOP or
                                                      igra > self.tip_igre or
                                                      igra == self.tip_igre and igralec == s_prednostjo}
                igra = igralec.licitiraj(self.igralci, seznam_licitacij, na_izbiro)
                seznam_licitacij.append((igralec.id, igra))
                if igra.ime != KLOP:
                    pomo.append(igralec)
                else:
                    self.aktivni_igralec = igralec
                    self.tip_igre = igra
            aktivni_licitatorji = [igralec for igralec in pomo]

    def poskrbi_za_talon(self):
        k = self.tip_igre.iz_talona
        if k > 0:
            moznosti = [self.talon[k * i:k * (i + 1)] for i in range(6 // k)]
            self.pobrano_iz_talona = self.aktivni_igralec.izberi_iz_talona(moznosti)
            self.aktivni_igralec.zamenjaj_s_talonom(self.pobrano_iz_talona)

    def odigraj_runde(self) -> None:
        prvi = 1
        if self.tip_igre in {BERAC, ODPRTI_BERAC, SOLO_BREZ}:
            prvi = self.igralci.index(self.aktivni_igralec)
        n = len(self.igralci)
        poteze = []  # type: List[List[Tuple[Igralec, Karta]]]
        for runda in range(self.st_rund):
            poteze.append([])
            for j in range(n):
                igralec = self.igralci[(prvi + j) % n]
                karta = igralec.odigraj_potezo(self.igralci, poteze, self.tip_igre, self.pobrano_iz_talona)
                poteze[-1].append((igralec, karta))
            zmagovalec_stiha = self.kdo_je_pobral(poteze[-1])
            stipendija = self.talon[runda:runda + 1] if self.tip_igre == KLOP else []  # bo prazno po 6 rundah
            zmagovalec_stiha.poberi_stih([karta for _, karta in poteze[-1]] + stipendija)

    def kdo_je_pobral(self, stih: List[Tuple[Igralec, Karta]]):
        # TODO: podpora barvnega valata, ko bo treba  ...
        opti = 0
        for i in range(1, len(stih)):
            if stih[i][1] > stih[opti][1]:
                opti = i
        return stih[opti][0]

    def prestej_tocke(self) -> None:
        if self.aktivni_igralec.st_pobranih_stihov in [0, self.st_rund]:
            aktivni_valat = self.aktivni_igralec.st_pobranih_stihov == self.st_rund
            for igralec in self.igralci:
                tocke = VSE_TOCKE if aktivni_valat == (igralec == self.aktivni_igralec) else 0
                self.tocke[igralec] = tocke
        else:
            for igralec in self.igralci:
                vsota = 0
                for stih in igralec.pobrano:
                    for karta in stih:
                        vsota += karta.tockovna_vrednost
                self.tocke[igralec] = round(vsota)
            # bonusi
            ekipe = [[igralec for igralec in self.igralci if (self.aktivni_igralec == igralec) == tf] for tf in [True, False]]
            for ekipa in ekipe:
                for bonus in BONUSI:
                    if bonus != BONUS_PAGAT_ULTIMO:  # TODO: kako je s pogatom
                        pobrano_ekipa = [stih for igralec in ekipa for stih in igralec.pobrano]
                        if bonus.pogoj(pobrano_ekipa):
                            for igralec in ekipa:
                                self.tocke[igralec] += bonus.vrednost  # TODO: napovedani

    def odigraj_igro(self):
        kupcek = [karta for karta in KARTE]
        self.mesalec.premesaj(kupcek)
        self.privzigovalec.privzdigni(kupcek)

        self.talon = self.mesalec.razdeli(kupcek, self.igralci)  # po tem trenutku imajo vsi igralci svoje karte

        self.licitacija()

        self.poskrbi_za_talon()

        self.odigraj_runde()

        self.prestej_tocke()
