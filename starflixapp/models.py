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

class Movies(models.Model):
    

    title=models.TextField(max_length=100)
    movie_desc=models.TextField(max_length=300)
    movie_image=models.ImageField(upload_to='movie_image/')
    movie_thumbnail=models.ImageField(upload_to='movie_thumbnail/')
    movie_genres=models.TextField(max_length=300)
    imdb_rating=models.FloatField()
    movie_duration=models.TextField(max_length=300)
    movie_genres=models.TextField(max_length=300)
    casts = models.ManyToManyField(Cast)
    crew = models.ManyToManyField(Crew)
    Tags = models.ManyToManyField(Tags)
    upload_date = models.DateTimeField(auto_now_add=True)
    movie_trailer = models.FileField(upload_to='Movies_Trailers/')
    movie_file = models.FileField(upload_to='Movie_File/')
    def __str__(self):
        return self.title
    

    