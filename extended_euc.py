def extended_euc(a,b):
    if a>b:
        r0=a
        r1=b
    else:
        r0=b
        r1=a
    r2=1
    q2=0
    q1=0
    q0=0
    s0=1
    s1=0
    s2=0
    t0=0
    t1=1
    while r2!=0:
        r2 = r0 % r1
        q2 = r0 // r1
        t2 = t0 - q2*t1
        s2 = s0-q2*s1
        s0,s1 = s1,s2
        t0,t1=t1,t2
        r0,r1=r1,r2
        q0,q1 = q1,q2
    print("S {} T {} Q {}".format(s0,t0,r0))
    if a>b:
        return s0,t0,q0
    else:
        return t0,s0,q0

    
