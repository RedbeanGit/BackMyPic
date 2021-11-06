#    This file is part of picdo.

#    picdo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    picdo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with picdo.  If not, see <https://www.gnu.org/licenses/>.

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
			'version': views.VERSION,
			'appName': views.TITLE
		}),
		name='login'
	),
	# logout
	url(r'^logout/$', 
		LogoutView.as_view(extra_context={
			'title': 'Déconnecté',
			'version': views.VERSION,
			'appName': views.TITLE
		}),
		name='logout'
	)
]
