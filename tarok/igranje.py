from ogrodje.odlocanje.matej import potezaMatej, licitacijaMatej

from ogrodje.igralec import Igralec
from ogrodje.odlocanje.definicije.funkcija_poteze import FunkcijaPoteze
from ogrodje.odlocanje.definicije.licitacijska_funkcija import LicitacijskaFunkcija
from ogrodje.odlocanje.implementacije.butelj import nakljucnaPoteza, nakljucnaLicitacija
from ogrodje.tarok import Tarok

matej = Igralec(False, 2, FunkcijaPoteze(potezaMatej), LicitacijskaFunkcija(licitacijaMatej))
butelj = Igralec(False, 3, FunkcijaPoteze(nakljucnaPoteza), FunkcijaPoteze(nakljucnaLicitacija))
butelj2 = Igralec(False, 43, FunkcijaPoteze(nakljucnaPoteza), FunkcijaPoteze(nakljucnaLicitacija))


igra = Tarok([butelj2, matej, butelj])
igra.odigraj_igro()





