from random import *
#from matej import taktikaMatej
from tomaz import taktikaTomaz

n = 10
k = 2

def nakljucna(spomin, odkriti, neodkriti, mojipari, tvojipari, bednapoteza):
    mozni = {x for x in neodkriti}
    for x in odkriti.values():
        mozni |= x
    print(mozni)
    i = choice(list(mozni))
    j = choice(list(mozni-{i}))
    return (i,j)


#dvoboj = [taktikaMatej, taktikaTomaz]
testT = [nakljucna, nakljucna]


def igra(k,n,strat,prvi):
    spomin = k*list(range(n))
    shuffle(spomin)
    print(spomin)
    print()
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
        print(i,j)
        print(odkriti)
        print(neodkriti)
        print(najdeni)
        print(predprejsnja,prejsnjaNicNovih)
        print()
        
    return najdeni
        
    
    
