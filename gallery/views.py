import math
import re
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
from .models import Picture, Album
from .utils import get_illegible_name

VERSION = '0.3.1'


def get_or_create_album(**filters):
	if Album.objects.filter(**filters).exists():
		album = Album.objects.get(**filters)
	else:
		album = Album(**filters)
		album.save()
	return album


class GalleryView(LoginRequiredMixin, View):
	template_name = 'gallery/gallery.html'
	view_name = 'gallery:gallery'

	def render(self, request, form):
		album = get_or_create_album(user=request.user, category='S', name='gallery')

		context = {
			'title': 'BackMyPic',
			'version': VERSION,
			'logged': True,
			'viewName': self.view_name,
			'selected': 'gallery',
			'form': form,
			'album': album
		}

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		return self.render(request, PictureForm())

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
		for pk in request.POST['ids'].strip().split(','):
			if pk.isdigit():
				pk = int(float(pk))
				picture = get_object_or_404(Picture, pk=pk, user=request.user)
				yield picture

	def hide_pictures(self, request, *args, **kwargs):
		filters = {'user': request.user, 'category': 'S'}
		album_gallery = get_or_create_album(**filters, name='gallery')
		album_hidden = get_or_create_album(**filters, name='hidden')

		for picture in self.loop_pictures_from_request(request):
			picture.hidden = True
			picture.save()

			if album_gallery.pictures.filter(pk=picture.pk).exists():
				album_gallery.pictures.remove(picture)

			if not album_hidden.pictures.filter(pk=picture.pk).exists():
				album_hidden.pictures.add(picture)
		album_gallery.save()
		album_hidden.save()
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
		if not request.POST['ids'].strip():
			return redirect('gallery:gallery')
			
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
		form = PictureForm(request.POST, request.FILES)

		if form.is_valid():
			album = get_or_create_album(user=request.user, category='S', name='gallery')
			images = request.FILES.getlist('image')

			for image in images:
				picture = Picture(image=image, user=request.user, filename=image.name)
				picture.save()
				album.pictures.add(picture)
			album.save()

			return redirect('gallery:gallery')
		return self.render(request, form)


class AlbumsView(LoginRequiredMixin, View):
	template_name = 'gallery/albums.html'
	view_name = 'gallery:albums'

	def get(self, request, *args, **kwargs):
		albums = Album.objects.filter(user=request.user)

		context = {
			'title': 'Albums - BackMyPic',
			'version': VERSION,
			'logged': True,
			'viewName': self.view_name,
			'selected': 'albums',
			'albums': albums
		}

		return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, View):
	template_name = 'gallery/settings.html'
	view_name = 'gallery:settings'

	def get(self, request, *args, **kwargs):
		context = {
			'title': 'Paramètres - BackMyPic',
			'version': VERSION,
			'logged': True,
			'viewName': self.view_name,
			'selected': 'settings'
		}

		return render(request, self.template_name, context)


class DetailsView(LoginRequiredMixin, View):
	template_name = 'gallery/details.html'
	view_name = 'gallery:details'
	model = Picture

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('picture_id', -1)
		picture = get_object_or_404(self.model, pk=pk)

		if picture.user != request.user:
			return HttpResponseForbidden()

		context = {
			'title': 'Photo - BackMyPic',
			'version': VERSION,
			'logged': True,
			'viewName': self.view_name,
			'picture': picture
		}

		return render(request, self.template_name, context)


class SearchView(LoginRequiredMixin, View):
	template_name = 'gallery/search.html'
	view_name = 'gallery:search'

	def get(self, request, *args, **kwargs):
		question = request.GET.get('query')
		pictures = []

		if question:
			words = question.split()

			for word in words:
				pictures += list(Picture.objects.filter(user=request.user, tags__icontains=word))

		context = {
			'title': 'Recherche - BackMyPic',
			'version': VERSION,
			'logged': True,
			'viewName': self.view_name
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return self.get(request, *args, **kwargs)


class RegisterView(View):
	template_name = 'registration/register.html'
	view_name = 'gallery:register'
	form = UserCreationForm

	def render(self, request, form):
		context = {
			'title': 'Créer un compte - BackMyPic',
			'version': VERSION,
			'logged': False,
			'viewName': self.view_name,
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
			user = form.save()
			login(request, user)

			return redirect('gallery:gallery')

		return self.render(request, form)