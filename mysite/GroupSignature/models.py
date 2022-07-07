from django.db import models

from django.db import models

# Create your models here.

class PublicKey(models.Model):
    N = models.CharField(max_length=1000)
    G = models.CharField(max_length=1000)
    H = models.CharField(max_length=1000)
    Z = models.CharField(max_length=1000)
    L = models.CharField(max_length=1000)
    L1 = models.CharField(max_length=1000)
    L2 = models.CharField(max_length=1000)
    LG = models.CharField(max_length=1000)
    K = models.CharField(max_length=1000)
    ESP = models.CharField(max_length=1000)
    Y = models.CharField(max_length=1000)


class PrivateKey(models.Model):
    P = models.CharField(max_length=1000)
    Q = models.CharField(max_length=1000)
    X = models.CharField(max_length=1000)


class Member(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    tildeE = models.CharField(max_length=1000)
    tildeZ = models.CharField(max_length=1000)
    u = models.CharField(max_length=1000, default='0')
    IsJoin = models.IntegerField(default=0)
