from .ogrodje.tarok import Tarok
from .ogrodje.igralec import Igralec
from .ogrodje.odlocanje.matej import taktikaMatej
from .ogrodje.odlocanje.butelj import nakljucnaTaktika


tomaz = Igralec(False, 1, taktikaMatej)
matej = Igralec(False, 2, taktikaMatej)
butelj = Igralec(False, 3, nakljucnaTaktika)


igra = Tarok([tomaz, matej, butelj])
igra.odigraj()





