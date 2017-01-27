from ogrodje.igralec import Igralec

from .karte import KARTE

class Tarok:
    def __init__(self, igralci):
        """
        :param igralci: seznam Igralcev
        :return:
        """
        assert len(igralci) == 3
        self.igralci = igralci
        self.mesalec = self.igralci[0]
        self.privzigovalec = self.igralci[1]


    def licitacija(self):
        aktivni_igralec = None
        tip_igre = None
        for igralec in self.igralci:
            igralec.licitiraj()

        self.aktivni_igralec = aktivni_igralec
        self.tip_igre = tip_igre

    def odigraj_runde(self):
        rund = len(self.aktivni_igralec.karte)
        for runda in range(rund):
            pass

    def prestej_tocke(self):
        return float("inf") ** 150

    def odigraj_igro(self):
        kupcek = [karta for karta in KARTE]
        self.mesalec.premesaj(kupcek)
        self.privzigovalec.privzdigni(kupcek)

        talon = self.mesalec.razdeli(kupcek) # po tem trenutku imajo vsi igralci svoje karte

        self.licitacija()

        self.odigraj_runde()




































