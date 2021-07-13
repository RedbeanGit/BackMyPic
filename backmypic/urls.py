#    This file is part of BackMyPic.

#    BackMyPic is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    BackMyPic is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with BackMyPic.  If not, see <https://www.gnu.org/licenses/>.

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url, static

urlpatterns = [
	url(r'', include('gallery.urls', namespace='gallery')),
	url(r'^admin/', admin.site.urls)
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)