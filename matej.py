from random import *
def p(m, k):
        return min(1, m / k)
def pp(k):
    return 1 / k
def nasprotnik(znani, neznani, stJaz, stOn, aliStSt, spomincek):
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

def verj(kaj, m, k, ig1, ig2, prejPra):
##    print("verj",kaj, m, k, ig1, ig2, prejPra)
    """kaj = 1 (zmaga), 0 (izen), -1 (poraz),
       m,k = stevilo znanih, neznanih polj
       ig1, ig2 = moj, tuj rezultat
       prejPra = T/F in pove, ali je bila prejšnja prazna."""
    klj = (kaj, m, k, ig1, ig2, prejPra)
    if klj in slovar:
        return slovar[klj]
   
    vred = None
    if kaj != 0:
        if m >= k:
            konc = ig1 + (m + k)//2
            if kaj == 1:
                vred = int(konc > ig2)
            else:
                vred = int(konc < ig2)
        elif m == 0:
            #sv/sv
            vred = verjSvSv(kaj, m, k, ig1, ig2, prejPra)
        else:# m >= 1, k >= 2
            #sv/sv ali sv/st
##            svsv = p(m, k) * operator(verj(kaj, m - 1, k - 1, ig1 + 1, ig2, False),
##                                      1 - (verj(kaj, m + 1, k - 1, ig2, ig1, False) + verj(0, m + 1, k - 1, ig2, ig1, False )))#odkriješ par in ga vzameš/pustiš
            #privzamemo, da potencialni par vedno vzameš
            svsvZ = verjSvSv(1, m, k, ig1, ig2, prejPra)
            svsvP = verjSvSv(-1, m, k, ig1, ig2, prejPra)
            svstZ = verjSvSt(1, m, k, ig1, ig2, prejPra)
            svstP = verjSvSt(-1, m, k, ig1, ig2, prejPra)
            if svsvZ + svstP > svstZ + svsvP:#da ni odštevanja ... boljše svsv
                vred = [svsvZ, svsvP]
            else:
                vred = [svstZ, svstP]
            #tu je vred optimalnejši par verjetnosti za sv/?
            if m >= 2:
                ststZ = verjStSt(1, m, k, ig1, ig2, prejPra)
                ststP = verjStSt(-1, m, k, ig1, ig2, prejPra)
                if vred[0] + ststP > ststZ + vred[1]:
                    vred = vred[kaj == -1]#če poraz, vzamemo zadnjo, sicer prvo komp.
                else:
                    vred = [ststZ, ststP][kaj == -1]
            else:
                vred = vred[kaj == -1]
        slovar[klj] = vred
        return vred
    else:
        return 1 - (verj(1, m, k, ig1, ig2, prejPra) + verj(-1, m, k, ig1, ig2, prejPra))

def verjSvSv(kaj, m, k, ig1, ig2, prejPra):
##    print("svsv", kaj, m, k, ig1, ig2, prejPra)
    #deluje za kaj = +-1 in kaj = 0, ker je -0 = 0 itd.
    assert k >= 2
    p1 = p(m, k)
    q1 = 1 - p1
    p2 = pp(k - 1)
    q2 = 1 - p2
    if m == 0:
        svsv = p2 * verj(kaj, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(-kaj, m + 2, k - 2, ig2, ig1, False)
    else:
        svsv = p1 * verj(kaj, m - 1, k - 1, ig1 + 1, ig2, False) + q1 * (p2 * verj(kaj, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(-kaj, m + 2, k - 2, ig2, ig1, False))
    return svsv

def verjSvSt(kaj, m, k, ig1, ig2, prejPra):
##    print("svst", kaj, m, k, ig1, ig2, prejPra)
    assert k >= 1 and m >= 1
    p1 = p(m, k)
    q1 = 1 - p1
    p2 = pp(k - 1)
    q2 = 1 - p2
    svst = p1 * verj(kaj, m - 1, k - 1, ig1 + 1, ig2, False) + q1 * verj(-1, m + 1, k - 1, ig2, ig1, False)
    return svst

def verjStSt(kaj, m, k, ig1, ig2, prejPra):
##    print("stst", kaj, m, k, ig1, ig2, prejPra)
    assert m >= 2
    if prejPra:
        if kaj == 1:
            return int(ig1 > ig2)
        elif kaj == -1:
            return int(ig1 < ig2)
        else:
            return int(ig1 == ig2)
    else:
        return verj(-kaj, m, k, ig2, ig1, True)    
    
    

def taktikaMatej(znani, neznani, ig1, ig2, aliStSt, spomincek):
    """Za kriterijsko funkcijo je treba vzet E[st točk na igro] = p(zmaga) - p(poraz)"""
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
    lst = list(neznani)
##    print("    lst =", lst)

    if m == 0:#"prva poteza"
##        print("    moram dva sveža ... m = 0")
        i = int(k * random())
        j = int((k - 1) * random())
        if j >= i: j +=1
        return (lst[i],lst[j])
    else:
        if m >= k:
##            print("    neznanih ni več kot znanih ... uganemo vse")
            i = int(k * random())
            prvi = lst[i]#neki neznani
            drugi = list(znani[spomincek[prvi]])[0]
            return (prvi, drugi)
        else:
            if m == 1:#k >= 2
                #sv/st ali sv/sv
                i = int(k * random())
                prvi = lst[i]
                drugi = None
                if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
    ##                  print("    obstaja tudi par")
                    drugi = list(znani[spomincek[prvi]])[0]#ker je itak sam en not
                if drugi == None:
    ##                  print("    ni para.")
                    #trenutno poznamo m + 1 in neznanih je k - 1
                    p2 = pp(k - 1)
                    q2 = 1 - p2
                    svsvZ = p2 * verj(1, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(-1, m + 2, k - 2, ig2, ig1, False)
                    svsvP = p2 * verj(-1, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(1, m + 2, k - 2, ig2, ig1, False)
                    svstZ = verj(-1, m + 1, k - 1, ig2, ig1, False)
                    svstP = verj(1, m + 1, k - 1, ig2, ig1, False)
                    if svsvZ + svstP > svstZ + svsvP:#da ni odštevanja ... boljše svsv
##                        print("    bolj se splača še eno ugibat")
                        j = int((k - 1) * random())
                        j += int(j >= i)
                        drugi = lst[j]
                    else:
##                        print("    raje prazno ...")
                        drugi = prazniKand[0]
                return (prvi, drugi)
            else:
                #vse tri na izbiro
                svsvZ = verjSvSv(1, m, k, ig1, ig2, aliStSt)
                svsvP = verjSvSv(-1, m, k, ig1, ig2, aliStSt)
                
                svstZ = verjSvSt(1, m, k, ig1, ig2, aliStSt)
                svstP = verjSvSt(-1, m, k, ig1, ig2, aliStSt)
                
                ststZ = verjStSt(1, m, k, ig1, ig2, aliStSt)
                ststP = verjStSt(-1, m, k, ig1, ig2, aliStSt)

                if ststZ + svsvP > svsvZ + ststP and ststZ + svstP > svstZ + ststP:
                    print("    prazna poteza ...")
                    return tuple(prazniKand[0])
                else:
                    i = int(k * random())
                    prvi = lst[i]
                    drugi = None
                    if spomincek[prvi] in znani and len(znani[spomincek[prvi]]) > 0:
    ##                  print("    obstaja tudi par")
                        drugi = list(znani[spomincek[prvi]])[0]#ker je itak sam en not
                    if drugi == None:
    ##                  print("    ni para.")
                        #trenutno poznamo m + 1 in neznanih je k - 1
                        p2 = pp(k - 1)
                        q2 = 1 - p2
                        svsvZ = p2 * verj(1, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(-1, m + 2, k - 2, ig2, ig1, False)
                        svsvP = p2 * verj(-1, m, k - 2, ig1 + 1, ig2, False) + q2 * verj(1, m + 2, k - 2, ig2, ig1, False)
                        svstZ = verj(-1, m + 1, k - 1, ig2, ig1, False)
                        svstP = verj(1, m + 1, k - 1, ig2, ig1, False)
                        if svsvZ + svstP > svstZ + svsvP:#da ni odštevanja ... boljše svsv
##                            print("    bolj se splača še eno ugibat")
                            j = int((k - 1) * random())
                            j += int(j >= i)
                            drugi = lst[j]
                        else:
##                        print("    raje prazno ...")
                            drugi = prazniKand[0]
                    return (prvi, drugi)
                              
            
            
def igra(k,n, str1, str2):
##    seed(10)
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
        (i,j) = f(odkriti, neodkriti, najdeni[igralec], najdeni[1 - igralec], prejsnjaNicNovih, spomin)
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
    for i in range(ponovi):
        if i%100 == 0:print(i)
        if i%2 == 0:
            x = igra(2, n, str1, str2)
        else:
            x = igra(2, n, str2, str1)
        if x[i%2] > x[1-i%2]:
            a[0] += 1
        elif x[i%2] < x[1-i%2]:
            a[1] += 1
        else:
            a[2] += 1
    return a

