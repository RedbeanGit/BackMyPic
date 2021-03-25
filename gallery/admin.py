from django.contrib.admin import site

from .models import Album, Picture

site.register(Album)
site.register(Picture)