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
    

slovar = {}

def verj(kaj, m, k, p1, p2, prejPra):
    """kaj = 1 (zmaga), 0 (izen), -1 (poraz),
       m,k = stevilo znanih, neznanih polj
       p1, p2 = moj, tuj rezultat
       prejPra = T/F in pove, ali je bila prejšnja prazna."""
    def p(m, k):
        return min(1, m/k)
    def pp(k):
        return 1/k
    klj = (kaj, m, k, p1, p2, prejPra)
    if klj in slovar:
        return slovar[klj]
   
    vred = None
    if kaj != 0:
        if m >= k:
            konc = p1 + (m + k)//2
            if kaj == 1:
                vred = int(konc > p2)
            else:
                vred = int(konc < p2)
        elif m == 0:
            #sv/sv
            vred = pp(k - 1) * verj(kaj, m, k - 2, p1 + 1, p2, False) + (1 - pp(k - 1)) * (1 - (verj(0, m + 2, k - 2, p2, p1, False) + verj(kaj, m + 2, k - 2, p2, p1, False)))
        elif m == 1:#k >= 2
            #sv/sv ali sv/st
            operator = [max, min][kaj == -1]
##            svsv = p(m, k) * operator(verj(kaj, m - 1, k - 1, p1 + 1, p2, False),
##                                      1 - (verj(kaj, m + 1, k - 1, p2, p1, False) + verj(0, m + 1, k - 1, p2, p1, False )))#odkriješ par in ga vzameš/pustiš
            #privzamemo, da potencialni par vedno vzameš
            svsv = p(m, k) * verj(kaj, m - 1, k - 1, p1 + 1, p2, False)
            svst = svsv
            svsv += (1 - p(m, k)) * (pp(k - 1) * verj(kaj, m, k - 2, p1 + 1, p2, False) + (1 - pp(k - 1)) * (1 - verj(kaj, m + 2, k - 2, p2, p1, False) - verj(0, m + 2, k - 2, p2, p1, False)))
            svst += (1 - p(m, k)) * (1 - verj(0, m + 1, k - 1, p2, p1, False) - verj(kaj, m + 1, k - 1, p2, p1, False))
            vred = operator(svsv, svst)
            
        elif m >= 2:
            #sv/sv ali sv/st ali st/st
            #SKOPIRANO OD m == 1
            #sv/sv ali sv/st
            operator = [max, min][kaj == -1]
##            svsv = p(m, k) * operator(verj(kaj, m - 1, k - 1, p1 + 1, p2, False),
##                                      1 - (verj(kaj, m + 1, k - 1, p2, p1, False) + verj(0, m + 1, k - 1, p2, p1, False )))#odkriješ par in ga vzameš/pustiš
            #privzamemo, da potencialni par vedno vzameš
            svsv = p(m, k) * verj(kaj, m - 1, k - 1, p1 + 1, p2, False)
            svst = svsv
            svsv += (1 - p(m, k)) * (pp(k - 1) * verj(kaj, m, k - 2, p1 + 1, p2, False) + (1 - pp(k - 1)) * (1 - verj(kaj, m + 2, k - 2, p2, p1, False) - verj(0, m + 2, k - 2, p2, p1, False)))
            svst += (1 - p(m, k)) * (1 - verj(0, m + 1, k - 1, p2, p1, False) - verj(kaj, m + 1, k - 1, p2, p1, False))

            if prejPra:
                stst = [int(p1 < p2), int(p1 > p2)][kaj == 1]
            else:
                stst = 1 - (verj(kaj, m, k, p2, p1, True) + verj(0, m, k, p2, p1, True))
            vred = operator(svsv, svst, stst)
        slovar[klj] = vred
        return vred
    else:
        return 1 - (verj(1, m, k, p2, p1, prejPra) + verj(-1, m, k, p2, p1, prejPra))

def taktikaMatej(znani, neznani, stJaz, stOn, aliStSt, spomincek):
    """Za kriterijsko funkcijo je treba vzet E[st točk na igro] = p(zmaga) - p(poraz)"""
    def p(m, k):
        return min(1, m / k)
    def pp(k):
        return 1 / k
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
        razSvSv = pp(k - 1) * (verj(1, m, k - 2, p1 + 1, p2, False) - verj(0, m, k - 2, p1 + 1, p2, False)) + (1 - pp(k - 1)) * (verj(1, m + 2, k - 2, p2, p1, False) - verj(-1, m + 2, k - 2, p2, p1, False))
    if k >= 1 and m >= 1:
        #sv/st
        razSvSt = verj(1, m + 1, k - 1, p2, p1, False) - verj(-1, m + 1, k - 1, p2, p1, False)
        
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
                if razSvSt > razSvSv:
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
                        if razSvSt > razSvSv:
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
                    d = max(razSvSv, razSvSt)
                    if d > 0:#s to igro pridobim
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
                            if razSvSt > razSvSv:
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
                #DO TU SEM KOKER TOK ZIHER; OD TU NAPREJ JE ŠE TREBA
                razStSt = verj(1, m, k, p1, p2)
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





















