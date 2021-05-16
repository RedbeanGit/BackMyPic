from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url, static

urlpatterns = [
	url(r'', include('gallery.urls', namespace='gallery')),
	url(r'^admin/', admin.site.urls)
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)