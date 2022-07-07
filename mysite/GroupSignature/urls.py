from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage.as_view(), name="home"),
    path('login/', views.LoginClass.as_view(), name="login"),
    path('signup/', views.signup.as_view(), name='signup'),
    path('publickey/', views.downpublickey, name='publickey'),
    path('generate/', views.checkGenerate.as_view(), name='checkgenerate'),
    path('generate/<int:id>', views.generate.as_view(), name='generatesignature'),
    path('checksignature', views.checksignature.as_view(), name='checksignature'),



    path('manager/', views.managerhomepage, name='manage'),
    path('manager/resetgroup/', views.reset, name='reset'),
    path('manager/privatekey/', views.downprivatekey, name='reset'),
    path('manager/showrequest/<int:request_page>', views.showrequests, name='showrequest'),
    path('manager/request/<int:memberID>', views.showrequest, name='show_member'),
    path('manager/accept/<int:memberID>', views.acceptmember, name='accept_member'),
    path('manager/delete/<int:memberID>', views.deletemember, name='delete_member'),
    path('manager/showmember/<int:member_page>', views.showmembers, name='showmembers'),
    path('manager/member/<int:memberID>', views.showmember, name='showmember'),
    path('manager/tracing', views.tracing.as_view(), name='tracing'),
]