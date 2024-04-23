from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Movies) 
admin.site.register(Cast) 
admin.site.register(Crew)
admin.site.register(Tags)
admin.site.register(Genre)
admin.site.register(TVShow)
admin.site.register(Season)
admin.site.register(Episode)