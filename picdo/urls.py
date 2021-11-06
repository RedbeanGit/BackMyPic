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

from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url, static

urlpatterns = [
	url(r'', include('gallery.urls', namespace='gallery')),
	url(r'^admin/', admin.site.urls)
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)