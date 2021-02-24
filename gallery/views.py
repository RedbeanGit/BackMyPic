from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.base import View

from .forms import ErrorList, PictureForm
from .models import Picture


class GalleryView(LoginRequiredMixin, View):
	template_name = 'gallery/gallery.html'
	model = Picture
	form = PictureForm

	def render(self, request, form):
		pictures = self.model.objects.filter(user__username=request.user.username)		
		context = {
			'title': 'BackMyPic',
			'col_len': 5,
			'search': True,
			'form': form,
			'pictures': pictures,
			'pic_count': pictures.count()
		}

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		return self.render(request, self.form())

	def post(self, request, *args, **kwargs):
		if 'delete' in request.POST:
			for pk in request.POST['delete'].split(','):
				if pk.isdigit():
					picture = get_object_or_404(Picture, pk=int(float(pk)))

					if picture.user == request.user:
						picture.delete()
			return redirect('gallery:gallery')

		form = self.form(request.POST, request.FILES)

		if form.is_valid():
			images = request.FILES.getlist('image')

			for image in images:
				picture = self.model(image=image, user=request.user, filename=image.name)
				picture.save()
			return redirect('gallery:gallery')
		return self.render(request, form)


class PictureView(LoginRequiredMixin, View):
	template_name = 'gallery/picture.html'
	model = Picture

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('picture_id', -1)
		picture = get_object_or_404(self.model, pk=pk)

		if picture.user != request.user:
			return HttpResponseForbidden()

		context = {
			'title': 'Photo - BackMyPic',
			'search': False,
			'picture': picture
		}

		return render(request, self.template_name, context)


class SearchView(LoginRequiredMixin, View):
	template_name = 'gallery/search.html'

	def get(self, request, *args, **kwargs):
		question = request.GET.get('query')
		pictures = []

		if question:
			words = question.split()

			for word in words:
				pictures += list(Picture.objects.filter(user=request.user, tags__icontains=word))

		context = {
			'pictures': pictures,
			'title': 'BackMyPic',
			'pic_count': len(pictures),
			'col_len': 5,
			'search': True
		}

		return render(request, self.template_name, context)


class SettingView(LoginRequiredMixin, View):
	template_name = 'gallery/settings.html'

	def get(self, request, *args, **kwargs):
		context = {
			'title': 'Paramètres - BackMyPic',
			'search': False
		}

		return render(request, self.template_name, context)


class RegisterView(View):
	template_name = 'registration/register.html'
	form = UserCreationForm

	def render(self, request, form):
		context = {
			'title': 'Créer un compte - BackMyPic',
			'search': False,
			'form': form
		}
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('gallery:gallery')
		return self.render(request, self.form())

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST, error_class=ErrorList)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('gallery:gallery')

		return self.render(request, form)