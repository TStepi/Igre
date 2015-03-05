from random import *
#from matej import taktikaMatej
from tomaz import taktikaTomaz

n = 10
k = 2

def nakljucna(spomin, odkriti, neodkriti, mojipari, tvojipari, bednapoteza):
    #print("Naključnež")
    mozni = {x for x in neodkriti}
    for x in odkriti.values():
        mozni |= x
    i = choice(list(mozni))
    j = choice(list(mozni-{i}))
    return (i,j)


def igra(k,n,strat,prvi):
    spomin = k*list(range(n))
    shuffle(spomin)
    #print(spomin)
    #print()
    odkriti = {i:set() for i in range(n)}
    neodkriti = set(range(k*n))
    igralec = prvi
    prejsnjaNicNovih = False
    predprejsnja = False

    najdeni = [0, 0]

    while sum(najdeni) < n and (not predprejsnja or not prejsnjaNicNovih):
        (i,j) = strat[igralec](spomin,odkriti,neodkriti,najdeni[igralec],najdeni[igralec-1],prejsnjaNicNovih)
        predprejsnja = prejsnjaNicNovih
        prejsnjaNicNovih = False
        odkriti[spomin[i]].add(i)
        odkriti[spomin[j]].add(j)
        if spomin[i] == spomin[j]:
            najdeni[igralec] += 1
            del odkriti[spomin[i]]
        else:
            igralec = 1 - igralec
            #če smo izbrali stare in nismo dobili para:
            if not (i in neodkriti or j in neodkriti):
                prejsnjaNicNovih = True
        neodkriti -= {i,j}
        #print(i,j)
        #print(odkriti)
        #print(neodkriti)
        #print(najdeni)
        #print(predprejsnja,prejsnjaNicNovih)
        #print()
        
    return najdeni
        
def test(n,taktika1,taktika2,st):
    """Naredi st simulacij igre spomina z n pari s strategijama taktika1 in taktika2, zacetni igralec se alternira. 
        Prvo število v seznamu je število zmag taktike1, drugo je število izenačenj, tretje pa število zmag taktike 2. """
    skupno = [0, 0, 0]
    strat = [taktika1, taktika2]
    for i in range(st):
        rezultat = igra(2,n,strat,i%2)
        if rezultat[0] > rezultat[1]:
            skupno[0] += 1
        elif rezultat[1] > rezultat[0]:
            skupno[2] += 1
        else:
            skupno[1] += 1
    print(skupno)
