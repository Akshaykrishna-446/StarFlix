# Create your models here.
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    userType=models.CharField(max_length=50)
    
    viewpassword=models.CharField(max_length=50,null=True)
    
    def _str_(self):
        return self.username

class user_reg(models.Model):
    
    user=models.OneToOneField(Login,on_delete=models.CASCADE,null=True)
    user_full_name=models.CharField(max_length=100,null=True)
    user_email=models.EmailField(null=True)
    user_username=models.TextField(null=True)
    user_password=models.TextField(null=True)
    user_cpassword=models.TextField(null=True)
    subscription=models.CharField(max_length=50,null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


class Cast(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields specific to cast members

    def __str__(self):
        return self.name

class Crew(models.Model):
    name = models.CharField(max_length=100)
    # Add other fields specific to crew members

    def __str__(self):
        return self.name
    
class Tags(models.Model):
    tag = models.CharField(max_length=100)
    # Add other fields specific to crew members

    def __str__(self):
        return self.tag
class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre
class Movies(models.Model):
    

    title=models.CharField(max_length=100)
    movie_desc=models.TextField(max_length=300)
    movie_image=models.ImageField(upload_to='movie_image/')
    movie_thumbnail=models.ImageField(upload_to='movie_thumbnail/')
    movie_genres = models.ForeignKey(Genre,on_delete=models.CASCADE,null=True)
    imdb_rating=models.FloatField()
    language=models.CharField(max_length=100,null=True)
    movie_mon_yr=models.TextField(max_length=30,null=True)
    movie_duration=models.TextField(max_length=10)
    ageGroup=models.TextField(max_length=4,null=True)
    casts = models.ManyToManyField(Cast)
    crew = models.ManyToManyField(Crew)
    Tags = models.ManyToManyField(Tags)
    upload_date = models.DateTimeField(auto_now_add=True)
    movie_trailer = models.FileField(upload_to='Movies_Trailers/')
    movie_file = models.FileField(upload_to='Movie_File/')
    trendingORpriority=models.IntegerField(default=0)

    def __str__(self):
        return self.title
    


class TVShow(models.Model):
    title = models.CharField(max_length=200)
    show_desc = models.TextField()
    TVShow_image=models.ImageField(upload_to='TVshow_image/')
    TVShow_thumbnail=models.ImageField(upload_to='TVshow_thumbnail/')
    TVShow_genre = models.ForeignKey(Genre,on_delete=models.CASCADE,null=True)
    howmanyseasons=models.IntegerField(null=True)
    language=models.CharField(max_length=100,null=True)
    imdb_rating=models.FloatField()
    TVShow_mon_yr=models.TextField(max_length=30,null=True)
    ageGroup=models.TextField(max_length=4,null=True)
    casts = models.ManyToManyField(Cast)
    crew = models.ManyToManyField(Crew)
    Tags = models.ManyToManyField(Tags)
    upload_date = models.DateTimeField(auto_now_add=True)
    TVshow_trailer = models.FileField(upload_to='TVshow_Trailers/')
    trendingORpriority=models.IntegerField(default=0)
    

    def __str__(self):
        return self.title
    


class Season(models.Model):
    show = models.ForeignKey(TVShow, on_delete=models.CASCADE, related_name='seasons',null=True)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.show.title} - Season {self.number}"

class Episode(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes',null=True)
    episode_title = models.CharField(max_length=200)
    episode_desc = models.TextField()
    number = models.IntegerField()
    TVShow_epi_image=models.ImageField(upload_to='TVshow_epi_image/', default='fortune_teller.jpg' )
    TVshow_epi_mon_yr=models.TextField(max_length=30,null=True)
    TVshow_epi_duration=models.TextField(max_length=10)
    TVshow_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return f"{self.season} -  episode - {self.number}"
    
class Favourite(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    movie_id=models.ForeignKey(Movies,on_delete=models.CASCADE,default=None)

class Watchlist(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    movie_id=models.ForeignKey(Movies,on_delete=models.CASCADE,default=None)

class FavouriteTV(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    tvs_id=models.ForeignKey(Episode,on_delete=models.CASCADE,default=None) 

class WatchlistTV(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    tvs_id=models.ForeignKey(Episode,on_delete=models.CASCADE,default=None)

class LastplayedMovie(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    movie_id=models.ForeignKey(Movies,on_delete=models.CASCADE,null=True)
    watched_at = models.DateTimeField(auto_now_add=True,null=True)

class LastplayedTV(models.Model):
    user_id=models.ForeignKey(user_reg,on_delete=models.CASCADE)
    epi_id=models.ForeignKey(Episode,on_delete=models.CASCADE,null=True)
    watched_at = models.DateTimeField(auto_now_add=True,null=True)
