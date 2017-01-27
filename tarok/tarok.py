from ogrodje.razno import *
from ogrodje.matej import taktikaMatej
from ogrodje.butelj import nakljucnaTaktika


tomaz = Igralec(False, 1, taktikaMatej)
matej = Igralec(False, 2, taktikaMatej)
butelj = Igralec(False, 3, nakljucnaTaktika)


igra = Tarok([tomaz, matej, butelj])
igra.odigraj()





