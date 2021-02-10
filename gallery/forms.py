from django import forms

from .models import User


class ErrorList(forms.utils.ErrorList):
	def __str__(self):
		return self.as_divs()

	def as_divs(self):
		if not self:
			return ''
		return '<div class="errorlist">{}</div>'.format( \
			''.join('<p>{}</p>'.format(e) for e in self)
		)


class UserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'required': True}),
			'password': forms.PasswordInput(attrs={'required': True})
		}

	def clean(self):
		cleaned_data = super(forms.ModelForm, self).clean()

		email = cleaned_data['email']
		password = cleaned_data['password']

		users = User.objects.filter(email=email.lower())

		if users.count():
			if users[0].password != password:
				self.add_error('password', 'Mot de passe incorrect !')
		else:
			self.add_error('email', 'Ce compte n\'existe pas !')

		return cleaned_data


class UserSigninForm(UserLoginForm):
	confirm_password = forms.CharField( \
		widget=forms.PasswordInput(attrs={'required': True})
	)

	def clean(self):
		cleaned_data = super(forms.ModelForm, self).clean()

		email = cleaned_data['email']
		password = cleaned_data['password']
		confirm_password = cleaned_data['confirm_password']

		users = User.objects.filter(email=email.lower())

		if users.count():
			self.add_error('email', 'Ce compte existe déjà !')

		if password != confirm_password:
			self.add_error('confirm_password', 'Les mots de passe ne correspondent pas !')

		return cleaned_data