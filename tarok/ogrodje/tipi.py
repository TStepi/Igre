KLOP = "klop"

ENA, DVA, TRI = "ena", "dva", "tri"
# SOLO_ENA, SOLO_DVA, SOLO_TRI = "solo_ena", "solo_dva", "solo_tri"
SOLO_BREZ = "solo_brez"
BERAC = "berac"
ODPRTI_BERAC = "odprti_berac"

VREDNOSTI_IGER = {KLOP: 0,
                  TRI: 10,
                  DVA: 20,
                  ENA: 30,
                  SOLO_BREZ: 50,
                  BERAC: 70,
                  ODPRTI_BERAC: 80}
IZ_TALONA = {KLOP: 0,
             TRI: 3,
             DVA: 2,
             ENA: 1,
             SOLO_BREZ: 0,
             BERAC: 0,
             ODPRTI_BERAC: 0}
assert sorted(VREDNOSTI_IGER.keys()) == sorted(IZ_TALONA.keys())


class TipIgre:
    def __init__(self, ime):
        assert ime in VREDNOSTI_IGER
        self.ime = ime
        self.vrednost = VREDNOSTI_IGER[ime]
        self.iz_talona = IZ_TALONA[ime]

    def __eq__(self, other):
        return self.vrednost == other.vrednost

    def __lt__(self, other):
        return self.vrednost < other.vrednost

IGRE = {ime: TipIgre(ime) for ime in VREDNOSTI_IGER} # type: Dict[str, TipIgre]
