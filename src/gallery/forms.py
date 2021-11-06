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

from django import forms

from .models import Picture


class ErrorList(forms.utils.ErrorList):
	def __str__(self):
		return self.as_divs()

	def as_divs(self):
		if not self:
			return ''
		return '<div class="errorlist">{}</div>'.format( \
			''.join('<p>{}</p>'.format(e) for e in self)
		)


class PictureForm(forms.ModelForm):
	class Meta:
		model = Picture
		fields = ('image',)
		widgets = {
			'image': forms.ClearableFileInput(attrs={
				'onchange': 'document.getElementById("upload-form").submit();',
				'multiple': True
			})
		}

