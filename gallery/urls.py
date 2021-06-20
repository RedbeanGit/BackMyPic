from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from gallery import views

app_name = 'gallery'

urlpatterns = [
	# gallery
	url(r'^$', 
		RedirectView.as_view(url='album/'), 
		name='gallery'
	),
	# picture
	url(r'^picture/(?P<picture_id>[0-9]+)/$',
		views.PictureView.as_view(),
		name='picture'
	),
	# album
	url(r'^album/$', 
		views.AlbumView.as_view(), 
		name='album'
	),
	url(r'^album/(?P<album_id>[0-9]+)/$', 
		views.AlbumView.as_view(), 
		name='album'
	),
	url(r'^album/(?P<album_id>[0-9]+)/(?P<page_id>[0-9]+)/$', 
		views.AlbumView.as_view(), 
		name='album'
	),
	# library
	url(r'^library/$', 
		views.LibraryView.as_view(), 
		name='library'
	),
	# settings
	url(r'^settings/$', 
		views.SettingsView.as_view(), 
		name='settings'
	),
	# register
	url(r'^register/$', 
		views.RegisterView.as_view(), 
		name='register'
	),
	# login
	url(r'^login/$', 
		LoginView.as_view(extra_context={
			'title': 'Connecte-toi',
			'version': views.VERSION
		}),
		name='login'
	),
	# logout
	url(r'^logout/$', 
		LogoutView.as_view(extra_context={
			'title': 'Déconnecté',
			'version': views.VERSION
		}),
		name='logout'
	)
]
