from random import *
from fractions import Fraction
def nasprotnik(znani, neznani, upanja, stJaz, stOn, aliStSt, spomincek):
    epsi = 10**-10
    prazniKand = [None, None]
    m = 0
    for st in znani:
        m += len(znani[st])
        if len(znani[st]) == 2:#če kdaj k != 2: TU PORRAVI ...
            return tuple(znani[st])
        elif len(znani[st]) > 0:
            prazniKand[int(prazniKand[0] != None)] = list(znani[st])[0]
    #v znanih sami različni      
    k = len(neznani)
    lst = list(neznani)
    i = int(k * random())
    prvi = lst[i]
    if spomincek[prvi] in znani and len(znani[spomincek[prvi]]):
        drugi = list(znani[spomincek[prvi]])[0]
    elif m > 0:
        drugi = prazniKand[0]
    else:
        j = int((k - 1) * random())
        j += j >= i
        drugi = lst[j]
    return (prvi, drugi)
    


def upanja(stParov):
    #sveže poteze: 0
    #stare: 1
    def p(m, k):
        return min(1, Fraction(m,k))
    n = 2 * stParov
    mat = [[[None, None] for i in range(n + 1)] for ii in range(n + 1)]
    #mat[m][k][prejsnja == prazna] = upanje, ko je m odkritih in k neodkritih | prejsnja = prazna

    #če m >= k: lahko pobereš vse ...
    for m in range(n + 1):
        for k in range(m + 1):
            if m + k <= n and (m + k)% 2 == 0:
                mat[m][k] = [(m + k)//2, (m + k)//2]#katere je itak vseen, bomo to v takitki premisll ...
            else:
                mat[m][k] = [None, None]

    #sicer pa rekurzija: najprej za X | True, potem pa še X | False
    for k in range(1, n + 1):
        for m in range(k%2, min(k, n - k + 1), 2):#m < k in m + k <= n ... prvi stolpec (k = 1) pustimo pri miru
##            print("m k =", m, k)
            #"prva poteza"
            if m == 0:#k > m in k sod ... k >= 2
                pr = Fraction(2 , k * (k - 1))
                #vrednosti mat[0][k][1] ne potrebujemo
                mat[0][k][0] = pr * (1 + mat[0][k - 2][0]) + (1 - pr) * (k//2 - mat[2][k - 2][0]) #izbrat moraš 2 sveži + prej ni bila prazna poteza
            elif m == 1:#k >= 2
                #sv/sv
                p1 = p(m, k)
                q1 = 1 - p1
                p2 = Fraction(1, k - 1)
                q2 = 1 - p2
                eSvSvTrue = p1 * (1 + mat[m - 1][k - 1][0]) + q1 * (p2 * (1 + mat[m][k - 2][0]) + q2 * ((k + m)//2 - mat[m + 2][k - 2][0]))
                #ali pa sv/st
##                print("mat[m,k]",mat[m][k])
                eSvStTrue = p1 * (1 + mat[m - 1][k - 1][0]) + q1 * ((k + m)//2 - mat[m + 1][k - 1][0])
                maksi = max(eSvSvTrue, eSvStTrue)
                mat[m][k][1] = maksi#ker ne moremo narediti (st, st) poteze
                mat[m][k][0] = maksi
            else:#k >= 2, m >= 2
                #sv/sv
                p1 = p(m, k)
                q1 = 1 - p1
                p2 = Fraction(1, k - 1)
                q2 = 1 - p2
                eSvSvTrue = p1 * (1 + mat[m - 1][k - 1][0]) + q1 * (p2 * (1 + mat[m][k - 2][0]) + q2 * ((k + m)//2 - mat[m + 2][k - 2][0]))
                #ali pa sv/st
                eSvStTrue = p1 * (1 + mat[m - 1][k - 1][0]) + q1 * ((k + m)//2 - mat[m + 1][k - 1][0])
                #ali pa st/st
                eStStTrue = 0
                mat[m][k][1] = max(eSvSvTrue, eSvStTrue, eStStTrue)#verjetno je zadnji (= 0) odveč ...
                mat[m][k][0] = max(eSvSvTrue, eSvStTrue, (k + m)//2 - mat[m][k][1])
##            print("po: ", mat[m][k])
    return mat
def izpisi(up):
    for x in up:
        for y in x:
            print("[{:.2f}, {:.2f}]".format(y[0] if y[0] != None else -1,  y[1] if y[1] != None else -1), end = "")
        print()
def taktikaMatej(znani, neznani, upanja, stJaz, stOn, aliStSt, spomincek):
    def p(m, k):
        return min(1,Fraction(m, k))
##    epsi = 10**-10
    prazniKand = [None, None]
    m = 0
    for st in znani:
        m += len(znani[st])
        if len(znani[st]) == 2:#če kdaj k != 2: TU PORRAVI ...
##            print("    Našel sem par že na začetku:", znani[st])
            return tuple(znani[st])
        elif len(znani[st]) > 0:
            prazniKand[int(prazniKand[0] != None)] = list(znani[st])[0]
    #v znanih sami različni      
    k = len(neznani)
##    print("    Imamo {} znanih in {} neznanih.".format(m, k))
    if k >= 2 and m >= 1:
        #sv/sv
        p1 = p(m, k)
        q1 = 1 - p1
        p2 = Fraction(1, k - 1)
        q2 = 1 - p2
        eSvSv = p1 * (1 + upanja[m - 1][k - 1][0]) + q1 * (p2 * (1 + upanja[m][k - 2][0]) + q2 * ((k + m)//2 - upanja[m + 2][k - 2][0]))
    if k >= 1 and m >= 1:
        #sv/st
        p1 = p(m, k)
        q1 = 1 - p1
        eSvSt = p1 * (1 + upanja[m - 1][k - 1][0]) + q1 * ((k + m)//2 - upanja[m + 1][k - 1][0])
        
    lst = list(neznani)
##    print("    lst =", lst)

    if m == 0:#"prva poteza"
##        print("    moram dva sveža ... m = 0")
        i = int(k * random())
        j = int((k - 1) * random())
        if j >= i: j +=1
        return (lst[i],lst[j])
    elif m == 1:
        if k == 1:
##            print("    m = k = 1, prisiljen v izbiro")
            return (list(neznani)[0], prazniKand[0])
        else:#k>=2 ...
##            print("    m = 1")
            i = int(k * random())
            prvi = lst[i]#neki neznani
##            print("    ugibam na", prvi, "in dobim", spomincek[prvi])
            drugi = None
            if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
##                print("    obstaja tudi par")
                drugi = list(znani[spomincek[prvi]])[0]#ker je itak sam en not
            if drugi == None:
##                print("    ni para.")
                if eSvSt > eSvSv:
##                    print("    bolj se splača staro ugibat")
                    drugi = prazniKand[0]
                else:
##                    print("    bolj se splača še eno ugibat")
                    j = int((k - 1) * random())
                    j += int(j >= i)
                    drugi = lst[j]
            return (prvi, drugi)

    else:
##        print("    imamo vsaj dva m-ja")
        if k <= m:#pol gremo ugant vse
##            print("    neznanih ni več kot znanih ... uganemo vse")
            i = int(k * random())
            prvi = lst[i]#neki neznani
            drugi = list(znani[spomincek[prvi]])[0]
            return (prvi, drugi)
        else:
            #m >= 2, k > m
            if aliStSt:
##                print("    nazadnje je bla prazna")
                if stJaz > stOn:
##                    print("    js sm zmagu ...")
                    return tuple(prazniKand)#zmaga ...
                elif stJaz < stOn:
##                    print("    trenutno zgublam")
                    #morm vsaj enga svežga
                    i = int(k * random())
                    prvi = lst[i]
##                    print("    ugibam na", prvi,"in dobim", spomincek[prvi])
                    drugi = None
                    if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
##                        print("    našel sem par")
                        drugi = list(znani[spomincek[prvi]])[0]
                    if drugi == None:
##                        print("    ni para.")
                        if eSvSt > eSvSv:
##                            print("    bolj se splača starega")
                            drugi = prazniKand[0]#itak vseen, katerga praznga zbereš
                        else:
##                            print("    boljs novega")
                            j = int((k - 1) * random())
                            j += int(j>= i)
                            drugi = lst[j]
                    return (prvi, drugi)
                else:#stJaz == stOn
##                    print("    tretnuno sva izenačena")
                    d = max(eSvSv, eSvSt)
                    if stJaz + d > stOn + (k + m)//2 - d:
##                        print("    splača se mi ugibat")
                        #se splača ugibat: skopiramo prejsnji razmislek
                        i = int(k * random())
                        prvi = lst[i]
##                        print("    ugibam na", prvi,"in dobim", spomincek[prvi])
                        drugi = None
                        if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
##                            print("    našel sem par")
                            drugi = list(znani[spomincek[prvi]])[0]
                        if drugi == None:
##                            print("    ni para.")
                            if eSvSt > eSvSv:
##                                print("    bolj se splača starega")
                                drugi = prazniKand[0]#itak vseen, katerga praznga zbereš
                            else:
##                                print("    boljs novega")
                                j = int((k - 1) * random())
                                j += int(j>= i)
                                drugi = lst[j]
                        return (prvi, drugi)
                    else:
                        #se ne splača ugibat
##                        print("    ne splača se mi ugibat")
                        return tuple(prazniKand)
            else:
##                print("    nazadne normalna poteza")
                eStSt = (k + m)//2 - upanja[m][k][1]
                m = max(eStSt, eSvSv, eSvSt)
                if eStSt == m:#itak mamo ful natančno
##                    print("    najboljš prazna")
                    return tuple(prazniKand)
                else:#ena od Sv/? je opti ... skopiramo zgornje
##                    print("    vsaj enga novga se splača")
                    i = int(k * random())
                    prvi = lst[i]
##                    print("    ugibam na", prvi,"in dobim", spomincek[prvi])
                    drugi = None
                    if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
##                        print("    našel sem par")
                        drugi = list(znani[spomincek[prvi]])[0]
                    if drugi == None:
##                        print("    ni para.")
                        if eSvSt > eSvSv:
##                            print("    bolj se splača starega")
                            drugi = prazniKand[0]#itak vseen, katerga praznga zbereš
                        else:
##                            print("    boljs novega")
                            j = int((k - 1) * random())
                            j += int(j>= i)
                            drugi = lst[j]
                    return (prvi, drugi)
            
            
            
def igra(k,n, str1, str2, upan = None):
##    seed(10)
    if upan == None:
        upan = upanja(n)
    strat = [str1,str2]
    spomin = k*list(range(n))
    shuffle(spomin)
    odkriti = {i:set() for i in range(n)}
    neodkriti = set(range(2*n))
    igralec = 0
    prejsnjaNicNovih = False
    predprej = False
    najdeni = [0, 0]
##    print("Začenjam igro.")
##    print("položaj:\n", spomin)
##    izpisi(upan)
    while sum(najdeni) < n and (not prejsnjaNicNovih or not predprej):
##        print()
##        print("Na potezi je igralec", igralec)
##        print("odkriti:", odkriti)
##        print("skriti:", neodkriti)
        predprej = prejsnjaNicNovih
        
        f = strat[igralec]
##        print(f.__name__)
        (i,j) = f(odkriti, neodkriti, upan, najdeni[igralec], najdeni[1 - igralec], prejsnjaNicNovih, spomin)
        prejsnjaNicNovih = False
##        print("Izbral je:", i, j)
        odkriti[spomin[i]].add(i)
        odkriti[spomin[j]].add(j)
        if spomin[i] == spomin[j]:
##            print("Našel je par! ")
            najdeni[igralec] += 1
            del odkriti[spomin[i]]
        else:
##            print("Zgrešil je! ")
            igralec = 1 - igralec
            #če smo izbrali stare in nismo dobili para:
            if not (i in neodkriti or j in neodkriti):
                prejsnjaNicNovih = True
        neodkriti -= {i,j}
    return najdeni

def test(ponovi, n, str1, str2):
    a = [0,0,0]
    up = upanja(n)
    for i in range(ponovi):
        if i%100 == 0:print(i)
        if i%2 == 0:
            x = igra(2, n, str1, str2, up)
        else:
            x = igra(2, n, str2, str1, up)
        if x[i%2] > x[1-i%2]:
            a[0] += 1
        elif x[i%2] < x[1-i%2]:
            a[1] += 1
        else:
            a[2] += 1
    return a





















