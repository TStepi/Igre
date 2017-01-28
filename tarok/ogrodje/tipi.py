klop = "klop"

ena, dva, tri = "ena", "dva", "tri"
# SOLO_ENA, SOLO_DVA, SOLO_TRI = "solo_ena", "solo_dva", "solo_tri"
solo_brez = "solo_brez"
berac = "berac"
odprti_berac = "odprti_berac"

VREDNOSTI_IGER = {klop: 0,
                  tri: 10,
                  dva: 20,
                  ena: 30,
                  solo_brez: 50,
                  berac: 70,
                  odprti_berac: 80}
IZ_TALONA = {klop: 0,
             tri: 3,
             dva: 2,
             ena: 1,
             solo_brez: 0,
             berac: 0,
             odprti_berac: 0}
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

    def __hash__(self):
        return self.ime.__hash__()

# tako hekanje povzroci nedelujoce importe:
#for ime in VREDNOSTI_IGER:
#    globals()[ime.upper()] = TipIgre(ime)
KLOP = TipIgre(klop)
TRI, DVA, ENA = TipIgre(tri), TipIgre(dva), TipIgre(ena)
SOLO_BREZ = TipIgre(solo_brez)
BERAC = TipIgre(berac)
ODPRTI_BERAC = TipIgre(odprti_berac)

IGRE = {KLOP, TRI, DVA, ENA, SOLO_BREZ, BERAC, ODPRTI_BERAC} # type: Set[TipIgre]

