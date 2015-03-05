def upanja(stParov):
    #sveže poteze: 1
    #stare: 0
    def p(m, k):
        return min(1, m/k)
    n = 2 * stParov
    mat = [[[0, 0, 0] for i in range(n + 1)] for ii in range(n + 1)]
    #mat[m][k] = upanje, ko je m odkritih in k neodkritih.

    #če m >= k: lahko pobereš vse ...
    for m in range(n + 1):
        for k in range(m + 1):
            mat[m][k][0] = (m + k)/2#katere je itak vseen, bomo to v takitki premisll ...

    #sicer pa rekurzija ...
    for k in range(1, n + 1):
        for m in range(k%2, min(k, n - k + 1), 2):
            if m == 0:#k gotovo sod
                p = 2 / (n * (n - 1))
                mat[0][k] = [p * (1 + mat[0][k - 2]) + (1 - p) * (k//2 - mat[2][k - 2]), 1, 1]#2 sveži
            else:
                #prva je sveža
                p1 = p(m, k)
                q1 = 1 - p1
                eSv = p1 * 1 + mat[m - 1][k - 1]
                    #še prištejemo:
                    #2. poteza = sveža:
                p2 = p(m + 1, k - 1)
                q2 = 1 - p2;
                pomo1 = p2 * (1 + mat[m][k - 2]) + q2 * ((m + k)//2 - mat[m + 2][k - 2])
                    #2. poteza = stari:
                pomo2 = (m + k)//2  - mat[m + 1][k - 1]
                potezaSv = [eSv + max(pomo1, pomo2), 1, int(pomo2 < pomo1)]
                #obe sta stari:
                #poračunamo posebi ...
                mat[m][k] = potezaSv[::]
    return mat

def taktikaMatej(znani, neznani, upanja, stJaz, stOn):
    m = 0
    unijaZn = []
    for st in znani:
        m += len(znani[st])
        if len(znani[st]) == 2:#če kdaj k != 2: TU PORRAVI ...
            return tuple(znani[st])
    #znanih sami različini
    k = len(neznani)
    if m == 0:#"prva poteza"
        lst = list(neznani)
        i = int(k * random())
        j = int((k - 1) * random())
        if j >= i: j +=1
        return (i,j)
    else:
        








        
            

