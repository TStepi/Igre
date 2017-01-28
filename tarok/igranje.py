from ogrodje.tarok import Tarok
from ogrodje.igralec import Igralec
from ogrodje.odlocanje.matej import potezaMatej, licitacijaMatej
from ogrodje.odlocanje.butelj import nakljucnaPoteza, nakljucnaLicitacija
from ogrodje.odlocanje.funkcija_poteze import FunkcijaPoteze
from ogrodje.odlocanje.licitacijska_funkcija import LicitacijskaFunkcija


matej = Igralec(False, 2, FunkcijaPoteze(potezaMatej), LicitacijskaFunkcija(licitacijaMatej))
butelj = Igralec(False, 3, FunkcijaPoteze(nakljucnaPoteza), FunkcijaPoteze(nakljucnaLicitacija))
butelj2 = Igralec(False, 43, FunkcijaPoteze(nakljucnaPoteza), FunkcijaPoteze(nakljucnaLicitacija))


igra = Tarok([butelj2, matej, butelj])
igra.odigraj_igro()





