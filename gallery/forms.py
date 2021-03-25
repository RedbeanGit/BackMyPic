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

