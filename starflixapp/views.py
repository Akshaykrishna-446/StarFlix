from django.shortcuts import redirect, render

# Create your views here.
from django.contrib.auth import authenticate,login,logout
from .models import *
# Create your views here.
def index(request):
    movie=Movies.objects.all()
    name=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        name=user.user_full_name
        
    context={
        'movie':movie,
        'name':name
    }
    
    return render(request,'index.html',context)
def moviesHome(request):

    movie=Movies.objects.all()
    context={
        'movie':movie
    }

    return render(request,'moviesHome.html',context)
def TVshows(request):


    return render(request,'TVshows.html')
def pricingpage(request):


    return render(request,'pricingpage.html')
def profile(request):


    return render(request,'profile.html')
def tags(request):


    return render(request,'tags.html')
def aboutUs(request):


    return render(request,'aboutUs.html')
def contactUs(request):


    return render(request,'contactUs.html')
def comingsoon(request):


    return render(request,'comingsoon.html')
def loginUser(request):
    if request.POST and 'register' in request.POST:
        fullname=request.POST["fullname"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["pass"]
        confirm_password=request.POST["cpass"]
        logine=Login.objects.create_user(username=username,
                                        password=password,
                                        userType='Customer',
                                        viewpassword=password)
        logine.save()
        obj=user_reg.objects.create(user=logine,
                                    user_full_name=fullname,
                                    user_email=email,
                                    user_username=username,
                                    user_password=password,
                                    user_cpassword=confirm_password
                                    )
        obj.save()
        return redirect('pricingpage')
    if request.POST and 'userlogin' in request.POST:
        username=request.POST["username"]
        password=request.POST["pass"]
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            request.session["userID"]=user.id
            return redirect('index')
       


    return render(request,'login.html')

def sign_out(request):
    logout(request)

    return redirect('index')
def All_movies(request):
    movie=Movies.objects.all()
    context={
        'movie':movie
    }

    return render(request,'All_movies.html',context)


def single_movie(request):
    

    return render(request,'single_movie.html')

