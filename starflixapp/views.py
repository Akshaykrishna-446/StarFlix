from itertools import chain
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.contrib.auth import authenticate,login,logout
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
    
    moviess=LastplayedMovie.objects.all()
    showss=LastplayedTV.objects.all()
    lastplayed = sorted(
        chain(moviess, showss),
        key=lambda instance: instance.watched_at,
        reverse=True
    )


    name=""
    
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=user_reg.objects.get(user__id=u_id)
        
        name=user1
        
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

def single_tvshow(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id) 
    episodes=Episode.objects.get(id=id)
    season_id=episodes.season.id
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
    context={
        'episode':episodes,
        'user':user,
        'related_show':related_epi
    }
    return render(request,'single_tvshow.html',context)

def allTvshows(request):

    tvshow=TVShow.objects.all()
    context={
        'tvshow':tvshow
    }

    return render(request,'allTvshows.html',context)
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

        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        if user:
            user.subscription=subc
            user.save()

    if request.POST and 'premium' in request.POST:

        subc="premium"

        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        if user:
            user.subscription=subc
            user.save()

    if request.POST and 'basic' in request.POST:

        subc="basic"

        u_id=request.session["userID"]
        user=user_reg.objects.get(user__id=u_id)
        if user:
            user.subscription=subc
            user.save()



    return render(request,'pricingpage.html')

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
        'user':user,
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

def single_movie(request,id):
    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    sub=user.subscription
    
    movie=Movies.objects.get(id=id)
    genre=movie.movie_genres
    related_movie=Movies.objects.filter(movie_genres=genre)
    

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
        

    context={
        'movie':movie,
        'related_movie':related_movie,
        'user':sub
    }

    return render(request,'single_movie.html',context)

""" def watch_movie(request, id):

    u_id=request.session["userID"]
    user=user_reg.objects.get(user__id=u_id)
    movie = Movies.objects.get(id=id)
    print('444444444444444444444444444444444444444444444')

    print(id)

    minutes_watched = int(request.POST.get('minutes_watched'))
    print('3333333333333333333333333333333333333333')

    print(minutes_watched)
    existing_entry = LastplayedMovie.objects.filter(movie_id=movie, user_id=user)
    if existing_entry:

        existing_entry.delete()

    if minutes_watched > 0:
  
        obj=LastplayedMovie.objects.create(movie_id=movie,
                                    user_id=user,
                                    minutes_watched=minutes_watched,
                                    )
        obj.save()

    return redirect('single_movie')
 """

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



