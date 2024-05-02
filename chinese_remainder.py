from extended_euc import *


n3=5
n2=11
n1=17
a3=2
a2=3
a1=5


m1,m2,q = extended_euc(n1,n2)

x1=a1+(a2-a1)*m1*n1

n2 = n1*n2
a2 = x1 % n2

print(n2)
print(n3)
m2,m3,q = extended_euc(n2,n3)

x=a2+(a3-a2)*m2*n2


print("Result {}".format(x%(n2*n3)))



