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

from django.test import TestCase
from django.shortcuts import reverse


class LibraryPageTestCase(TestCase):
	def test_library_view_get(self):
		response = self.client.get(reverse('gallery:library'))
		self.assertEqual(response.status_code, 302)


class AlbumPageTestCase(TestCase):
	def test_album_view_get(self):
		response = self.client.get(reverse('gallery:album'))
		self.assertEqual(response.status_code, 302)


class PicturePageTestCase(TestCase):
	def test_picture_view_get(self):
		picture_id = 1
		response = self.client.get(reverse('gallery:picture', args=(picture_id,)))
		self.assertEqual(response.status_code, 302)


class SettingsPageTestCase(TestCase):
	def test_settings_view_get(self):
		response = self.client.get(reverse('gallery:settings'))
		self.assertEqual(response.status_code, 302)