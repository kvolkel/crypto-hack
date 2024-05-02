from sage.all import *
import itertools
moduli=[]
residues=[]
with open("endless_emails.txt","r") as emails:
    for l in emails:
        if "n" in l:
            moduli.append(int(l.split("=")[1]))
        elif "c" in l:
            residues.append(int(l.split("=")[1]))

#if 3 people sent the same message, then we could do a cube root over the natural numbers to obtain the original message
for comb in itertools.combinations(range(0,7),3):
    m=[moduli[_] for _ in comb]
    r=[residues[_] for _ in comb]
    CRT=CRT_list(r,m)
    try:
        print("TRY")
        print(CRT.nth_root(3))
        print("FOUND ROOT")
    except:
        print("cant find root")
