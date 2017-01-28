from typing import Callable, List, Set

from ogrodje.karte import Karta


class IzbiralkaIzTalona:
    def __init__(self, funkcija: Callable[[Set[Karta], List[List[Karta]]], List[Karta]]) -> None:
        self.funkcija = funkcija

    def izracunaj(self,
                  igralceve_karte: Set[Karta],
                  deli_talona: List[List[Karta]]
                  ) -> List[Karta]:
        return self.funkcija(igralceve_karte, deli_talona)


class MenjalkaSTalonom:
    def __init__(self, funkcija: Callable[[Set[Karta], List[Karta]], Set[Karta]]) -> None:
        self.funkcija = funkcija

    def izracunaj(self,
                  igralceve_karte: Set[Karta],
                  izbrani_del_talona: List[Karta]
                  ) -> Set[Karta]:
        return self.funkcija(igralceve_karte, izbrani_del_talona)
