from itertools import chain
import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .models import *
# Create your views here.
def index(request):

    movie=Movies.objects.order_by('-trendingORpriority')[:5]
    popular_movie=Movies.objects.order_by('-imdb_rating')[:10]
    popular_tvshow=TVShow.objects.order_by('-imdb_rating')[:10]
    latest_movies=Movies.objects.order_by('-id')[:5]
    latest_tvshow=TVShow.objects.order_by('-id')[:5]
    trending_movies=Movies.objects.order_by('trendingORpriority')[:10]
    trending_tvshow=Episode.objects.all()
    
    All_movies=Movies.objects.all()
    trending_movie=Movies.objects.order_by('trendingORpriority')[:1]
    popular_content = sorted(
        chain(popular_movie, popular_tvshow),
        key=lambda instance: instance.id,
        reverse=True
    )[:10]
    
    


    name=""
    lastplayed=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1
        moviess=LastplayedMovie.objects.filter(user_id=user1)
        showss=LastplayedTV.objects.filter(user_id=user1)
        lastplayed = sorted(
        chain(moviess, showss),
        key=lambda instance: instance.watched_at,
        reverse=True
    )
        
    context={
        'movie':movie,
        'name':name,
        'lastplayed':lastplayed,
        'popular_content':popular_content,
        'latest_movies':latest_movies,
        'trending_movies':trending_movies,
        'latest_tvshow':latest_tvshow,
        'trending_movie':trending_movie,
        'trending_tvshow':trending_tvshow,
        'popular_tvshow':popular_tvshow,
        'All_movies':All_movies
    }
    
    return render(request,'index.html',context)

def moviesHome(request):
    movies=Movies.objects.order_by('trendingORpriority')[:5]
    movie=Movies.objects.all()
    latest_movie=Movies.objects.order_by('-id')[:4]
    popular_movie=Movies.objects.order_by('-imdb_rating')[:10]
    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1
    context={
        'name':name,
        'movie':movie,
        'latest_movie':latest_movie,
        'popular_movie':popular_movie,
        'movies':movies
        
    }

    return render(request,'moviesHome.html',context)

def TVshows(request):
    tvshows=TVShow.objects.order_by('trendingORpriority')[:5]
    Tvshow=TVShow.objects.all()
    popular_tvshow=TVShow.objects.order_by('-imdb_rating')[:10]
    latest_tvshow=TVShow.objects.order_by('-id')[:4]
    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1
    context={
        'name':name,
        'Tvshow':Tvshow,
        'popular_tvshow':popular_tvshow,
        'latest_tvshow':latest_tvshow,
        'tvshows':tvshows
        
        
    }
    return render(request,'TVshows.html',context)

def TVshow_details(request,id):
    season = request.GET.get('seasons')
    TVshow=TVShow.objects.get(id=id)
    seasons=Season.objects.filter(show=id)

    if request.method == 'POST':
        season_id = request.POST["season"]
        season=Episode.objects.filter(season=season_id)



    context={
        'TVshow':TVshow,
        'showcount':len(seasons),
        'seasons':seasons,
        'season':season,
        
        
    }
    
    return render(request,'TVshow_details.html',context)

@login_required(login_url='login')
def single_tvshow(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id) 
    episodes=Episode.objects.get(id=id)
    season_id=episodes.season.id

    reviews=TVReview.objects.filter(episode_id=episodes)
    total_reviews = TVReview.objects.filter(episode_id=episodes).count()
    total_rating = sum(review.rating for review in reviews)
    average = total_rating / len(reviews) if reviews else 0
    average_rating = round(average, 1)

    existing_entry = LastplayedTV.objects.filter(epi_id=episodes, user_id=user)
    
    if existing_entry:

        existing_entry.delete()
    obj=LastplayedTV.objects.create(epi_id=episodes,
                                    user_id=user
                                    )
    obj.save()

    related_epi=Episode.objects.filter(season=season_id).exclude(id=id)

    if 'fav' in request.POST:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        epi = Episode.objects.get(id=id)


        obj=FavouriteTV.objects.create(tvs_id=epi,
                                        user_id=user
                                        )
        obj.save()
        

    if 'watchlist' in request.POST:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        epi = Episode.objects.get(id=id)


        obj=WatchlistTV.objects.create(tvs_id=epi,
                                        user_id=user
                                        )
        obj.save()

    if 'review' in request.POST:
        
        content = request.POST['content']
        rating = request.POST['rating'] 
        episodes=Episode.objects.get(id=id)
       
        review = TVReview.objects.create(episode_id=episodes, content=content, rating=rating, user=user)
        review.save()

        




    context={
        'episode':episodes,
        
        'related_show':related_epi,
        'userDetails':user,
        'total_reviews':total_reviews,
        'average_rating':average_rating,
    }
    return render(request,'single_tvshow.html',context)

def allTvshows(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    tvshow=TVShow.objects.all()
    product_paginator=Paginator(tvshow,4)
    tvshow=product_paginator.get_page(page)

    context={
        'tvshow':tvshow
    }

    return render(request,'allTvshows.html',context)

def download_movie(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    file_path = movie.movie_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as movie_file:
            response = HttpResponse(movie_file.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    return redirect('index')

def download_tvshow(request, tvshow_id):
    tvshow = get_object_or_404(Episode, pk=tvshow_id)
    file_path = tvshow.TVshow_file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as tvshow_file:
            response = HttpResponse(tvshow_file.read(), content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    return redirect('index')

def searchresult(request):
    
    if 'search' in request.POST:
        query_name = request.POST['searched']
        if query_name:
            mresults = Movies.objects.filter(title__contains=query_name)
            tresults = TVShow.objects.filter(title__contains=query_name)
            results = sorted(
            chain(mresults, tresults),
            key=lambda instance: instance.id,
            reverse=True
            )
    
            context={
                "results":results,
            }
    

    return render(request,'searchresult.html',context)
def pricingpage(request):

    if request.POST and 'free' in request.POST:

        subc="free"
        if "userID" in request.session:
            u_id=request.session["userID"]
            user=user_reg.objects.get(user__id=u_id)
            if user:
                user.subscription=subc
                user.save()
                return redirect('index')

    if request.POST and 'premium' in request.POST:

        subc="premium"
        if "userID" in request.session:
            u_id=request.session["userID"]
            user=user_reg.objects.get(user__id=u_id)
            if user:
                user.subscription=subc
                user.save()
            return redirect('index')

    if request.POST and 'basic' in request.POST:

        subc="basic"
        if "userID" in request.session:
            u_id=request.session["userID"]
            user=user_reg.objects.get(user__id=u_id)
            if user:
                user.subscription=subc
                user.save()
            return redirect('index')



    return render(request,'pricingpage.html')

@login_required(login_url='login')
def profile(request):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)

    watchlist=Watchlist.objects.filter(user_id__id=user.id)
    watchlisttv=WatchlistTV.objects.filter(user_id__id=user.id)

    favourite=Favourite.objects.filter(user_id__id=user.id)
    favouritetv=FavouriteTV.objects.filter(user_id__id=user.id)
    
    bfavourite = sorted(
        chain(favourite, favouritetv),
        key=lambda instance: instance.id,
        reverse=True
    )    
    bwatchlist = sorted(
        chain(watchlist, watchlisttv),
        key=lambda instance: instance.id,
        reverse=True
    )    
    
    try:
        if request.method == 'POST' and request.FILES['profile_pic']:
            user_profile = user_reg.objects.get(user__id=u_id)
            user_profile.profile_pic = request.FILES['profile_pic']
            user_profile.save()
            return redirect('profile')
    except:
        return redirect('profile')

    context={
        'watchlist':bwatchlist,
        'favourite':bfavourite,
        'userdetails':user,
    }

    return render(request,'profile.html',context)

def tags(request):

    tags=Tags.objects.all()
    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1
    context={
        'name':name,
        'tags':tags
    }

    return render(request,'tags.html',context)

def tagsredirect(request,tag):
    try:


        tag_obj = Tags.objects.get(tag=tag)
        movies = Movies.objects.filter(Tags=tag_obj)
        tvshow = TVShow.objects.filter(Tags=tag_obj)

        catagory = sorted(
        chain(movies, tvshow),
        key=lambda instance: instance.id,
        reverse=True
        )

    except Tags.DoesNotExist:
        movies = []

    

    
    context={
        "catagory":catagory,
        'tag':tag,
    }
    return render(request,'category.html',context)
def category(request):


    return render(request,'category.html')
def aboutUs(request):

    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1

    context={
        'name':name,
    }
    return render(request,'aboutUs.html',context)

def contactUs(request):
    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1

    context={
        'name':name,
    }

    return render(request,'contactUs.html',context)

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
        return redirect('login')
    
    if request.POST and 'userlogin' in request.POST:
        username=request.POST["username"]
        password=request.POST["pass"]
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            request.session["userID"]=user.id
            u_id=request.session["userID"]
            user=user_reg.objects.get(user__id=u_id)
            paid=user.subscription
            if paid == "premium":
                 return redirect('index')
            elif paid == "basic":
                return redirect('index') 
            else:
                return redirect('pricingpage')
       


    return render(request,'login.html')

def sign_out(request):
    logout(request)

    return redirect('index')

def All_movies(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    movie=Movies.objects.all()
    product_paginator=Paginator(movie,4)
    movie=product_paginator.get_page(page)
    
    context={
        'movie':movie
    }

    return render(request,'All_movies.html',context)

@login_required(login_url='login')
def single_movie(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    sub=user.subscription
    
    movie=Movies.objects.get(id=id)
    genre=movie.movie_genres
    related_movie=Movies.objects.filter(movie_genres=genre)
    
    reviews=Review.objects.filter(movie_id=movie)
    total_reviews = Review.objects.filter(movie_id=movie).count()
    total_rating = sum(review.rating for review in reviews)
    average = total_rating / len(reviews) if reviews else 0
    average_rating = round(average, 1)

    existing_entry = LastplayedMovie.objects.filter(movie_id=movie, user_id=user)

    if existing_entry:

        existing_entry.delete()

    
    
    obj=LastplayedMovie.objects.create(movie_id=movie,
                                user_id=user,
                                
                                )
    obj.save()
    
    if 'fav' in request.POST:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        movie = Movies.objects.get(id=id)


        obj=Favourite.objects.create(movie_id=movie,
                                        user_id=user
                                        )
        obj.save()
        

    if 'watchlist' in request.POST:
        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        movie = Movies.objects.get(id=id)


        obj=Watchlist.objects.create(movie_id=movie,
                                        user_id=user
                                        )
        obj.save()

    if 'review' in request.POST:
        
        content = request.POST['content']
        rating = request.POST['rating'] 
        movie = Movies.objects.get(id=id)
       
        review = Review.objects.create(movie_id=movie, content=content, rating=rating, user=user)
        review.save()

        context={
            'movie':movie,
            'related_movie':related_movie,
            'usersub':sub,
            'userDetails':user,
            'total_reviews':total_reviews,
            'average_rating':average_rating,
        }
        return render(request,'single_movie.html',context)

    context={
        'movie':movie,
        'related_movie':related_movie,
        
        'userDetails':user,
        'total_reviews':total_reviews,
        'average_rating':average_rating,
    }

    return render(request,'single_movie.html',context)

@login_required(login_url='login')
def addToWatchlist(request,id):

    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    movie = Movies.objects.get(id=id)


    obj=Watchlist.objects.create(movie_id=movie,
                                    user_id=user
                                    )
    obj.save()

    return redirect('moviesHome')

def removeWatchlist(request,id):
    print('444444444444444444444444444444444444444444444')
    print(id)
    remove=Watchlist.objects.get(id=id)
        
    remove.delete() 
    return redirect('profile')

def removeWatchlistTV(request,id):

    remove=WatchlistTV.objects.get(id=id)
        
    remove.delete() 
    return redirect('profile')

@login_required(login_url='login')
def addToFavourite(request,id):

    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    movie = Movies.objects.get(id=id)


    obj=Favourite.objects.create(movie_id=movie,
                                    user_id=user
                                    )
    obj.save()

    return redirect('moviesHome')

def removeFavourite(request,id):
    print('444444444444444444444444444444444444444444444')
    print(id)
    remove=Favourite.objects.get(id=id)
        
    remove.delete() 
    return redirect('profile')

def removeFavouriteTV(request,id):
    remove=FavouriteTV.objects.get(id=id)
        
    remove.delete() 
    return redirect('profile')



