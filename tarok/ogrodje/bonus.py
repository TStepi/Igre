from typing import Callable, List, Set

from ogrodje.karte import Karta, KRALJI, TRULA, PALCKA


class Bonus:
    def __init__(self,
                 ime: str,
                 pogoj: Callable[[List[List[Karta]]], bool],
                 vrednost: int
                 ) -> None:
        self.ime = ime
        self.pogoj = pogoj
        self.vrednost = vrednost

    def __hash__(self):
        return self.ime.__hash__()


def vsi_prisotni(iskane: Set[Karta], stihi: List[List[Karta]]) -> bool:
    najdeni = 0
    for stih in stihi:
        for karta in stih:
            if karta in iskane:
                najdeni += 1
    return najdeni == len(iskane)


BONUS_KRALJI = Bonus("kralji", lambda pobrano: vsi_prisotni(KRALJI, pobrano), 10)
BONUS_TRULA = Bonus("trula", lambda pobrano: vsi_prisotni(TRULA, pobrano), 10)
BONUS_PAGAT_ULTIMO = Bonus("pagat_ultimo", lambda pobrano: PALCKA in pobrano[-1], 25)

BONUSI = {BONUS_KRALJI, BONUS_TRULA, BONUS_PAGAT_ULTIMO}