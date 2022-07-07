import os

from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import mimetypes
from .Services import SignatureService
from django.contrib.auth import authenticate, login, decorators
from .Utils import NumberUtil, KeyUtil
from .models import Member, PublicKey
from django.core.mail import send_mail, EmailMessage

fileFolderName= str(settings.BASE_DIR)+"/GroupSignature/Files/"
# Create your views here.

class homepage(View):
    def get(self, request):
        return render(request, 'core/core.html')

class LoginClass(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("pass")
        my_user = authenticate(username = username, password = password)
        if my_user is None:
            return render(request, "core/core.html")
        login(request, my_user)
        return HttpResponseRedirect("/manager/")

def downpublickey(request):
    filename= fileFolderName+"PublicKey.csv"
    path = open(filename, 'r')
    mime_type, _ = mimetypes.guess_type(filename)

    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=PublicKey.csv"

    return response

# Member
class signup(View):
    def get(self, request):
        return render(request, 'member/signup.html', {'noti':False, 'success':""})

    def post(self, request):
        
        name = request.POST.get("name")
        email = request.POST.get("email")
        try:
          f = request.FILES["file"]
          tildeE= str(f.readline()).split(",")[1].split("\\")[0]
          tildeZ= str(f.readline()).split(",")[1].split("\\")[0]
        except:
          return render(request, 'member/signup.html', {'noti': False, 'fnoti':"Your public key is fail"})

        check = Member.objects.filter(email = email).count()
        if (check>0):
            return render(request, 'member/signup.html', {'noti': True, 'success':""})
        else:
            rq = Member()
            rq.name= name
            rq.email= email
            rq.tildeE = tildeE
            rq.tildeZ= tildeZ
            rq.IsJoin= 0
            rq.save()
            return render(request, 'member/signup.html', {'noti': False, 'success':"Your request has been sent to admin"})


# Manager

@decorators.login_required(login_url="/login/")
def managerhomepage(request):
    check = PublicKey.objects.all().count()
    a=False
    if check==0:
        a=True

    print(check)
    return render(request, 'manager/manager.html', {'check':a})

@decorators.login_required(login_url="/login")
def downprivatekey(request):
    filename= fileFolderName+"PrivateKey.csv"
    path = open(filename, 'r')
    mime_type, _ = mimetypes.guess_type(filename)

    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=PrivateKey.csv"

    return response

@decorators.login_required(login_url="/login/")
def showrequests(request, request_page):
    list_request= Member.objects.filter(IsJoin=0)
    minValue = (request_page-1)*5;
    maxValue= min(minValue+5, len(list_request))
    page = len(list_request)/5;
    page= int(page)
    if (len(list_request)%5!=0):
        page=page+1
    pages= range(1,page+1)

    return render(request, 'manager/requests.html', {"list_request":list_request[minValue:maxValue],'pages':pages})

@decorators.login_required(login_url="/login/")
def showrequest(request, memberID):
    member= Member.objects.filter(id=memberID)
    return render(request, 'manager/request.html', {"member": member[0]})

@decorators.login_required(login_url="/login/")
def reset(request):
    SignatureService.Setup()
    Member.objects.all().delete()
    return HttpResponseRedirect("/manager/")

def acceptmember(request, memberID):
    private = KeyUtil.GetPrivate()
    p = int(private.P)
    q= int(private.Q)
    phi= (p-1)*(q-1)
    n= p*q

    instance = Member.objects.get(id=memberID)
    tildeE = int(instance.tildeE)
    tildeZ= int(instance.tildeZ)

    invertedE = pow(tildeE, -1, phi)
    u = pow(tildeZ, invertedE, n)

    instance.u = str(u)
    instance.IsJoin = 1
    instance.save()

    return HttpResponseRedirect("/manager/showrequest/1")

def deletemember(request, memberID):
    page=1
    instance = Member.objects.get(id=memberID)
    list_request = Member.objects.filter(IsJoin=0)
    n = len(list_request)
    for i in range(n):
        if (list_request[i].id == memberID):
            page= i
    if (page%5==0):
        page= int(page/5)+1
    instance.delete();
    return HttpResponseRedirect("/manager/showrequest/"+str(page))

@decorators.login_required(login_url="/login/")
def showmembers(request, member_page):
    list_request= Member.objects.filter(IsJoin=1)
    minValue = (member_page-1)*5;
    maxValue= min(minValue+5, len(list_request))
    page = len(list_request)/5;
    page= int(page)
    if (len(list_request)%5!=0):
        page=page+1
    pages= range(1,page+1)

    return render(request, 'manager/members.html', {"list_request":list_request[minValue:maxValue],'pages':pages})

@decorators.login_required(login_url="/login/")
def showmember(request, memberID):
    member= Member.objects.filter(id=memberID)
    return render(request, 'manager/member.html', {"member": member[0]})


class checkGenerate(View):
    def get(self, request):
        return render(request, 'member/checkgenerate.html',{"noti":""})

    def post(self, request):
        email = request.POST.get("email")
        record= Member.objects.filter(email= email)

        if (record.count()==0):
            return render(request, 'member/checkgenerate.html',{"noti":"Email "+email+" is not a member of group "})
        else:
            if record[0].IsJoin==0:
                return render(request, 'member/checkgenerate.html', {"noti": "Your enrollment request has not been approved by the manager"})
            else:
                return HttpResponseRedirect(str(record[0].id))


class generate(View):
    def get(self, request, id):
        record= Member.objects.filter(id=id)
        return render(request, 'member/generate.html',{"member":record[0]})

    def post(self, request, id):
        privatekey = request.FILES["privatekey"]
        e= str(privatekey.readline()).split(",")[1].split("\\")[0]
        record = Member.objects.filter(id=id).first()
        email_1= record.email
        u = record.u
        try:
            check = SignatureService.CheckMemberKey(int(u), int(e))
            if (check == True):
                f = request.FILES["file"]
                message = f.read()
                (c, s1, s2, s3, a, b, d) = SignatureService.GenerateSignature(int(u), int(e), message)
                email2= request.POST.get("r-email")
                email = EmailMessage("Signature", "", 'Trung10052014@gmail.com', [email_1, email2])
                email.content_subtype = 'html'
                KeyUtil.CreateSignatureFile(c, s1, s2, s3, a, b, d)
                email.attach_file(fileFolderName + "Signature.csv")
                email.attach(f.name, message, f.content_type)
                email.send()
                KeyUtil.DeleteSignatureFile()

                return render(request, 'member/generate.html',{"member": record, "noti": "Your file is signed, please check your email"})
            else:
                return render(request, 'member/generate.html',{"member": record, "key_error": "Your private key is incorrect"})
        except:
            return render(request, 'member/generate.html',{"member": record, "error": "An error occurred, please try again"})


class checksignature(View):
    def get(self, request):
        return render(request, 'receive/checksignature.html')

    def post(self, request):
        signature = request.FILES["signature"]
        try:
            (c,s1,s2,s3,a,b,d) = KeyUtil.ParseSignature(signature)
            file = request.FILES["file"]
            message = file.read()
            check = SignatureService.Verifying(c, s1, s2, s3, a, b, d, message)
            if (check):
                return render(request, 'receive/checksignature.html', {"success": True})
            else:
                return render(request, 'receive/checksignature.html', {"fail": True})
        except:
            return render(request, 'receive/checksignature.html',{"signature_error": True})
        
        
class tracing(View):
    def get(self, request):
        return render(request, 'manager/tracing.html')

    def post(self, request):
        signature = request.FILES["signature"]
        try:
            (c,s1,s2,s3,a,b,d) = KeyUtil.ParseSignature(signature)
            u = SignatureService.tracing(c,s1,s2,s3,a,b,d)
            check = Member.objects.filter(u=str(u)).count()
            if (check>0):
                record = Member.objects.filter(u=str(u)).first()
                return render(request, 'manager/tracing.html', {"success": record })
            else:
                return render(request, 'manager/tracing.html', {"fail": True})
        except:
            return render(request, 'manager/tracing.html',{"signature_error": True})


        
