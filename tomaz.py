from random import choice

def taktikaTomaz(spomin, odkriti, neodkriti, mojipari, tvojipari, safety):
    #print("Tomaž")
    pogledani = set()
    izbira = ()
    for p in odkriti:
        pogledani |= odkriti[p]
        if len(odkriti[p]) == 2:
            izbira = tuple(odkriti[p])
    if izbira != ():
        return izbira
        
    i = choice(list(neodkriti))
    prva = spomin[i]
    if len(odkriti[prva]) == 1:
        return tuple([i]+list(odkriti[prva]))
        
    elif pogledani:
        return (i,choice(list(pogledani)))
    else:
        return (i,choice(list(neodkriti-{i})))
