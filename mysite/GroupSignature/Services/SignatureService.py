import django
django.setup()
from ..models import PublicKey, PrivateKey, Member
import  random
from ..Utils import NumberUtil, KeyUtil
import hashlib
import pathlib



def Hash(m):
    a=str(m)
    result=hashlib.sha512(a.encode('utf-8')).digest()
    return int.from_bytes(result, 'little')

def ChooseG(n, upperBlock):
    while True:
        number = NumberUtil.GetPrime(NumberUtil.lower(n), upperBlock)
        if number < upperBlock:
            return number
        else:
            continue

def Setup(lg=1200,ep=9/8,l=1200,l1=860,l2=600):
    PublicKey.objects.all().delete()
    PrivateKey.objects.all().delete()

    p = NumberUtil.GetPrime(NumberUtil.lower(lg / 2), NumberUtil.upper(lg / 2))
    q = NumberUtil.GetPrime(NumberUtil.lower(lg / 2), NumberUtil.upper(lg / 2))
    k = 256
    n = p * q
    g = ChooseG(lg - 1, n)

    hatZ = NumberUtil.nBitRandom(NumberUtil.lower(lg), NumberUtil.upper(lg))
    z = pow(g, hatZ, n)
    hatH = NumberUtil.nBitRandom(NumberUtil.lower(lg), NumberUtil.upper(lg))
    h = pow(g, hatH, n)

    x = random.randrange(0, NumberUtil.upper(lg))
    y = pow(g, x, n)



    KeyUtil.SavePublicKey(KeyUtil.Public(n,g,h,z,l,l1,l2,lg,k,ep,y))
    KeyUtil.SavePrivate(KeyUtil.Private(p,q,x))

def Registration():
    public= KeyUtil.GetPublicKey()

    hatE = NumberUtil.GetPrime(NumberUtil.lower(int(public.L)), NumberUtil.upper(int(public.L)))
    e = NumberUtil.GetPrime(2**int(public.L1)+1, 2**int(public.L1)+2**int(public.L2) - 1)
    tempE = hatE*e
    tempZ = pow(int(public.Z), hatE, int(public.N))



    return (e,tempE, tempZ)

def Hash(m):
    a=str(m)
    result=hashlib.sha512(a.encode('utf-8')).digest()
    return int.from_bytes(result, 'little')

def CheckMemberKey(u, e):
    publickey = KeyUtil.GetPublicKey()
    z= int(publickey.Z)
    n = int(publickey.N)
    temp = pow(u,e,n)
    z= z % n
    return (temp==(z % n))

def GenerateSignature(u, e, message):
    publickey = KeyUtil.GetPublicKey()
    lg =int(publickey.LG)
    g = int(publickey.G)
    n = int(publickey.N)
    y= int(publickey.Y)
    h = int(publickey.H)
    z= int(publickey.Z)
    ep = float(publickey.ESP)
    l2= int(publickey.L2)
    l1= int(publickey.L1)
    k= int(publickey.K)

    m = Hash(message)
    w = random.randrange(0, 2 ** lg)

    a = pow(g, w, n)
    b = (u * pow(y, w, n)) % n
    d = (pow(g, e, n) * pow(h, w, n)) % n
    r1 = random.randrange(0, pow(2, int(ep * (l2 + k))))
    r2 = random.randrange(0, pow(2, int(ep * (lg + l1 + k))))
    r3 = random.randrange(0, pow(2, int(ep * (lg + k))))
    t1 = (pow(b, r1, n) * pow(pow(y, r2, n), -1, n)) % n
    t2 = (pow(a, r1, n) * pow(pow(g, r2, n), -1, n)) % n
    t3 = pow(g, r3, n)
    t4 = (pow(g, r1, n) * pow(h, r3, n)) % n
    c = Hash(str(g) + str(h) + str(y) + str(z) + str(a) + str(b) + str(d) + str(t1) + str(t2) + str(t3) + str(t4) + str(m))
    s1 = r1 - c * (e - 2 ** l1)
    s2 = r2 - c * e * w
    s3 = r3 - c * w

    return c, s1, s2, s3, a, b, d

def Verifying(c,s1,s2,s3,a,b,d, message):
    publickey = KeyUtil.GetPublicKey()
    lg = int(publickey.LG)
    g = int(publickey.G)
    n = int(publickey.N)
    y = int(publickey.Y)
    h = int(publickey.H)
    z = int(publickey.Z)
    ep = float(publickey.ESP)
    l2 = int(publickey.L2)
    l1 = int(publickey.L1)
    k = int(publickey.K)

    m = Hash(message)
    tempHat = int(s1 - c * 2 ** l1)
    t1 = pow(z, c, n) * pow(b, tempHat, n) * pow(pow(y, s2, n), -1, n)
    t2 = pow(a, tempHat, n) * pow(pow(g, s2, n), -1, n)
    t3 = pow(a, c, n) * pow(g, s3, n)
    t4 = pow(d, c, n) * pow(g, tempHat, n) * pow(h, s3, n)

    t1 = t1 % n
    t2 = t2 % n
    t3 = t3 % n
    t4 = t4 % n

    tempC = Hash(str(g) + str(h) + str(y) + str(z) + str(a) + str(b) + str(d) + str(t1) + str(t2) + str(t3) + str(t4) + str(m))

    return tempC == c

def tracing(c,s1,s2,s3,a,b,d):
    publickey = KeyUtil.GetPublicKey()
    n = int(publickey.N)

    privatekey = KeyUtil.GetPrivate()
    x= int(privatekey.X)
    result = b * pow(pow(a, x, n), -1, n)
    result = result % n

    return result
