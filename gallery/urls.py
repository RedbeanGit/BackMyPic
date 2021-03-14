"""backmypic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from gallery import views

app_name = 'gallery'

urlpatterns = [
	url(r'^$', views.GalleryView.as_view(), name='gallery'),
	url(r'^details/(?P<picture_id>[0-9]+)/$', views.DetailsView.as_view(), name='picture'),
	url(r'^search/$', views.SearchView.as_view(), name='search'),
	url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
	url(r'^register/$', views.RegisterView.as_view(), name='register'),
	url(r'^albums/$', views.AlbumsView.as_view(), name='albums')
]
