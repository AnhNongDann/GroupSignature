from django.contrib import admin

from .models import PublicKey, PrivateKey, Member
# Register your models here.

admin.site.register(PublicKey)
admin.site.register(PrivateKey)
admin.site.register(Member)