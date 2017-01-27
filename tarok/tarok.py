from .razno import *
from .matej import taktikaMatej
from .butelj import nakljucnaTaktika


tomaz = Igralec(False, taktikaMatej)
matej = Igralec(False, taktikaMatej)
butelj = Igralec(False, nakljucnaTaktika)


igra = Tarok([tomaz, matej, butelj])
igra.odigraj()





