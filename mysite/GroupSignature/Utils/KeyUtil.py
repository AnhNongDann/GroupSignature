import os

from ..models import PublicKey, PrivateKey

from django.conf import settings

fileFolderName= str(settings.BASE_DIR)+"/GroupSignature/Files/"

def SavePublicKey(public):
    record = PublicKey()

    record.N= public.N
    record.G= public.G
    record.H= public.H
    record.Z= public.Z
    record.L= public.L
    record.L1= public.L1
    record.L2= public.L2
    record.LG= public.LG
    record.K= public.K
    record.ESP= public.ESP
    record.Y= public.Y

    file = open(fileFolderName + "PublicKey.csv", "w")
    file.writelines("N,"+str(public.N) + "\n")
    file.writelines("G,"+str(public.G) + "\n")
    file.writelines("H,"+str(public.H) + "\n")
    file.writelines("Z,"+str(public.Z) + "\n")
    file.writelines("L,"+str(public.L) + "\n")
    file.writelines("L1,"+str(public.L1) + "\n")
    file.writelines("L2,"+str(public.L2) + "\n")
    file.writelines("LG,"+str(public.LG) + "\n")
    file.writelines("K,"+str(public.K) + "\n")
    file.writelines("ESP,"+str(public.ESP) + "\n")
    file.writelines("Y,"+str(public.Y) + "\n")
    file.close()

    record.save()

def SavePrivate(private):
    record = PrivateKey()
    record.P= private.P
    record.Q= private.Q
    record.X= private.X

    file = open(fileFolderName + "PrivateKey.csv", "w")
    file.writelines("P," + str(private.P) + "\n")
    file.writelines("Q," + str(private.Q) + "\n")
    file.writelines("X," + str(private.X) + "\n")
    file.close()

    record.save()

def GetPublicKey():
    record = PublicKey.objects.all().first()
    return record

def GetPrivate():
    record = PrivateKey.objects.all().first()
    return record

def Public(n,g,h,z,l,l1,l2,lg,k,esp,y):
    public = PublicKey()
    public.N = str(n)
    public.G = str(g)
    public.H = str(h)
    public.Z = str(z)
    public.L = str(l)
    public.L1 = str(l1)
    public.L2 = str(l2)
    public.LG = str(lg)
    public.K = str(k)
    public.ESP = str(esp)
    public.Y = y
    return public

def Private(p,q,x):
    private = PrivateKey()
    private.P = str(p)
    private.Q = str(q)
    private.X = str(x)

    return private

def CreateSignatureFile(c, s1, s2, s3, a, b, d):
    f = open(fileFolderName + "Signature.csv", 'a+')
    f.writelines("C," + str(c) + "\n")
    f.writelines("S1," + str(s1) + "\n")
    f.writelines("S2," + str(s2) + "\n")
    f.writelines("S3," + str(s3) + "\n")
    f.writelines("A," + str(a) + "\n")
    f.writelines("B," + str(b) + "\n")
    f.writelines("D," + str(d) + "\n")
    f.close()

def DeleteSignatureFile():
    os.remove(fileFolderName + "Signature.csv")

def ParseSignature(f):
    c= int(str(f.readline()).split(",")[1].split("\\")[0])
    s1= int(str(f.readline()).split(",")[1].split("\\")[0])
    s2= int(str(f.readline()).split(",")[1].split("\\")[0])
    s3= int(str(f.readline()).split(",")[1].split("\\")[0])
    a= int(str(f.readline()).split(",")[1].split("\\")[0])
    b= int(str(f.readline()).split(",")[1].split("\\")[0])
    d= int(str(f.readline()).split(",")[1].split("\\")[0])

    return (c,s1,s2,s3,a,b,d)
