from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.EmailBackEnd import EmailBackEnd


# Create your views here.
# def showDemoPage(request):
#     return render(request, "demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # Authenticate using the custom EmailBackEnd
        email = request.POST.get("email")  # Get the email input
        password = request.POST.get("password")  # Get the password input

        # Pass the arguments as keyword arguments to authenticate()
        user = EmailBackEnd().authenticate(request=request, username=email, password=password)
        if user!=None:
            login(request,user)

            if user.user_type=="1":
                # return HttpResponse("Email : " + request.POST.get("email") +" Password : "+request.POST.get("password"))
                return redirect('/admin_home')

            elif user.user_type=="2":
                # return HttpResponseRedirect(reverse("staff_home"))
                # return HttpResponse("staff login"+str(user.user_type))
                return redirect('/staff_home')
            else:
                # return HttpResponse("student login"+str(user.user_type))
                return redirect('/student_home')
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("/")
        

# def GetUserDetails(request):
#     if request.user!=None:
#         return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
#     else:
#         return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")