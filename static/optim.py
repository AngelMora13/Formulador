"""from cvxopt.modeling import op, variable
a=variable()
b=variable()
c=variable()
c3 = ((6*a+45*b+5*c)/400>=20)
c5 = ((6*a+45*b+5*c)/400<=22)

c4 = ((4*a+7*b+14*c)/400>=7)
c6 = ((4*a+7*b+14*c)/400<=8)

c7=((11*a+6*b+10*c)/400<=10)
c8=((11*a+6*b+10*c)/400>=9)

lp1 = op(a+b+c-400, [c3,c4,c5,c6,c7,c8])
lp1.solve()
lp1.status

print(round(a.value[0]))
print(round(b.value[0]))
print(round(c.value[0]))
"""
from cvxopt.modeling import op, variable
hola=[{"mat":"mat1","prot":10,"hum":5},{"mat":"mat2","prot":5,"hum":8},{"mat":"mat3","prot":3,"hum":4}]
obj=0
c1=0
c2=0
c3=0
for x in hola:
    x["mat"]=variable()
    obj+=x["mat"]
    c1+=x["prot"]*x["mat"]
    c2+=x["hum"]*x["mat"]
    c3+=x["mat"]
c3=(c3==30)
c2=c2/30<=7
c1 = c1/30>=8

c4=hola[2]["mat"]>=0
c5 = c1<=8.5
obj=obj
lp1=op(obj,[c1,c2,c3,c4])
print(lp1)
lp1.solve(verbose=True)
lp1.status

for x in hola:
    print(x["mat"].value[0])

