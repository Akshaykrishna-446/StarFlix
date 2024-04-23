from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('moviesHome', views.moviesHome, name='moviesHome'),
    path('TVshows', views.TVshows, name='TVshows'),
    path('TVshow_details/<id>', views.TVshow_details, name='TVshow_details'),
    path('pricingpage', views.pricingpage, name='pricingpage'),
    path('login/', views.loginUser, name='login'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
    path('tags/', views.tags, name='tags'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('contactUs/', views.contactUs, name='contactUs'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
    path('All_movies/', views.All_movies, name='All_movies'),
    path('single_movie/<id>', views.single_movie, name='single_movie'),
    path('addToWatchlist/<id>', views.addToWatchlist, name='addToWatchlist'),
    path('addToFavourite/<id>', views.addToFavourite, name='addToFavourite'),
    path('removeWatchlist/<id>', views.removeWatchlist, name='removeWatchlist'),
    path('removeFavourite/<id>', views.removeFavourite, name='removeFavourite'),
    
]