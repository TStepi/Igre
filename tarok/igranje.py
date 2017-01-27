from ogrodje.tarok import Tarok
from ogrodje.igralec import Igralec
from ogrodje.odlocanje.matej import potezaMatej, licitacijaMatej
from ogrodje.odlocanje.butelj import nakljucnaPoteza, nakljucnaLicitacija


matej = Igralec(False, 2, potezaMatej, licitacijaMatej)
butelj = Igralec(False, 3, nakljucnaPoteza, nakljucnaLicitacija)
butelj2 = Igralec(False, 43, )


igra = Tarok([tomaz, matej, butelj])
igra.odigraj()





