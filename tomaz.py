def taktikaTomaz(spomin, odkriti, neodkriti, mojipari, tvojipari, safety):
    pass
    
    
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
