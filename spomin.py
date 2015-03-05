from random import *
from matej import taktikaMatej


n = 10
k = 2




def igra(k,n):
    
    def strategija1():
        pogledani = set()
        izbira = ()
        for p in odkriti:
            pogledani |= odkriti[p]
            if len(odkriti[p]) == k:
                izbira = tuple(odkriti[p])
        if izbira != ():
            return izbira
        i = choice(list(preostali-pogledani))
        prva = spomin[i]
        if len(odkriti[prva]) == k-1:
            return tuple([i]+list(odkriti[prva]))
        
            

    def strategija2():
        i = choice(list(preostali))
        j = choice(list(preostali-{i}))
        return (i,j)
    
    strat = [strategija1,strategija2]
    spomin = k*list(range(n))
    shuffle(spomin)
    odkriti = {i:set() for i in range(n)}
    neodkriti = set(range(2*n))
    preostali = set(range(2*n))
    igralec = 0
    prejsnjaNicNovih = False

    najdeni = [0, 0]

    while preostali:
        f = strat[igralec]
        (i,j) = f()
        odkriti[spomin[i]].add(i)
        odkriti[spomin[j]].add(j)
        neodkriti -= {i,j}
        if spomin[i] == spomin[j]:
            najdeni[igralec] += 1
            preostali -= {i,j}
            odkriti[spomin[i]] = set()
        else:
            igralec = 1 - igralec

    return najdeni
        
    
    
