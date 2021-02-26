import os
import zipfile

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.base import View

from .forms import ErrorList, PictureForm
from .models import Picture
from .utils import get_illegible_name


class GalleryView(LoginRequiredMixin, View):
	template_name = 'gallery/gallery.html'
	model = Picture
	form = PictureForm

	def render(self, request, form):
		pictures = self.model.objects.filter(user__username=request.user.username, hidden=False)		
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
		actions = {
			'hide': self.hide_pictures,
			'delete': self.delete_pictures,
			'share': self.share_pictures,
			'download': self.download_pictures,
			'upload': self.upload_pictures
		}
		
		default_fct = lambda r, *a, **k: redirect('gallery:gallery')
		action = actions.get(request.POST['action'], default_fct)
		return action(request, *args, **kwargs)

	def loop_pictures_from_request(self, request):
		for pk in request.POST['ids'].split(','):
			if pk.isdigit():
				pk = int(float(pk))
				picture = get_object_or_404(Picture, pk=pk)

				if picture.user == request.user:
					yield picture

	def hide_pictures(self, request, *args, **kwargs):
		for picture in self.loop_pictures_from_request(request):
			picture.hidden = True
			picture.save()
		return redirect('gallery:gallery')

	def delete_pictures(self, request, *args, **kwargs):
		for picture in self.loop_pictures_from_request(request):
			picture.delete()
		return redirect('gallery:gallery')

	def share_pictures(self, request, *args, **kwargs):
		for picture in self.loop_pictures_from_request(request):
			pass
			# TODO: find a way to share pictures
		return redirect('gallery:gallery')

	def download_pictures(self, request, *args, **kwargs):
		zippath = settings.TMP_ROOT / 'zipfiles' / (get_illegible_name() + '.zip')
		filenames = set()

		with zipfile.ZipFile(zippath, 'w', compression=zipfile.ZIP_DEFLATED) as file:
			for picture in self.loop_pictures_from_request(request):
				filename = picture.filename
				
				if filename in filenames:
					name, ext = os.path.splitext(filename)
					filename = name + ' ({})' + ext
					index = 2

					while filename.format(index) in filenames:
						index += 1
					filename = filename.format(index)
				filenames.add(filename)
				file.write(picture.image.path, arcname=filename)
		
		return FileResponse(open(zippath, 'rb'), as_attachment=True, filename='Photos.zip')

	def upload_pictures(self, request, *args, **kwargs):
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