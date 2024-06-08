from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User 
from bot_home.models import AuthenticationId


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect("apikey/")
    return render(request,"oauth/login.html")


def apikey(request):
    if request.method == "POST": 
        authids = AuthenticationId.objects.all()
        authkey = authids.filter(user_mail=request.user)
        if not authkey:
            key = request.POST.get("int-token")
            id = request.POST.get("page-id")  
            userauth = AuthenticationId(user_mail = request.user,integration_key=key,page_title=id)
            userauth.save()
            return redirect("bot_home:chatbot_view")
        else:
            return redirect("bot_home:chatbot_view")
    else:
        authids = AuthenticationId.objects.all()
        authkey = authids.filter(user_mail=request.user)
        if authkey:
            return redirect("bot_home:chatbot_view")
        else:
            return render(request,'oauth/userdata.html')