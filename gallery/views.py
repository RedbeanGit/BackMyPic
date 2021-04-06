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
from .models import Picture, Album, UserSettings
from .utils import get_illegible_name

VERSION = '0.5.2'
TITLE = 'BackMyPic'


def get_or_create_album(**filters):
	if Album.objects.filter(**filters).exists():
		album = Album.objects.get(**filters)
	else:
		album = Album(**filters)
		album.save()
	return album


def get_or_create_user_settings(user):
	if UserSettings.objects.filter(user=user).exists():
		user_settings = UserSettings.objects.get(user=user)
	else:
		album = get_or_create_album(user=user, category='S', name='gallery')
		user_settings = UserSettings(user=user, current_album=album)
		user_settings.save()
	return user_settings


class BaseView(View):
	title = TITLE
	version = VERSION
	template_name = 'gallery/base.html'
	view_name = 'gallery:gallery'
	logged = True

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.get_base_context())

	def get_base_context(self):
		return {
			'title': self.title,
			'version': self.version,
			'viewName': self.view_name,
			'logged': self.logged
		}


class PictureView(LoginRequiredMixin, BaseView):
	title = 'Photo - ' + TITLE
	template_name = 'gallery/picture.html'
	view_name = 'gallery:picture'


class AlbumView(LoginRequiredMixin, BaseView):
	title = 'Album - ' + TITLE
	template_name = 'gallery/album.html'
	view_name = 'gallery:album'

	def render(self, request, form, album_id=None):
		if album_id is None:
			user_settings = get_or_create_user_settings(request.user)
			album = user_settings.current_album
		else:
			album = get_object_or_404(Album, pk=album_id, user=request.user)

		context = self.get_base_context()
		context['form'] = form
		context['album'] = album

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		return self.render(request, PictureForm(), kwargs.get('album_id', None))

	def post(self, request, *args, **kwargs):
		actions = {
			'hide': self.hide_pictures,
			'delete': self.delete_pictures,
			'share': self.share_pictures,
			'download': self.download_pictures,
			'upload': self.upload_pictures
		}
		
		default_fct = lambda r, *a, **k: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request, *args, **kwargs)

	def loop_pictures_from_request(self, request):
		for pk in request.POST['content'].strip().split(','):
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

		return redirect(self.view_name, **kwargs)

	def delete_pictures(self, request, *args, **kwargs):
		for picture in self.loop_pictures_from_request(request):
			picture.delete()
		return redirect(self.view_name, **kwargs)

	def share_pictures(self, request, *args, **kwargs):
		for picture in self.loop_pictures_from_request(request):
			pass
			# TODO: find a way to share pictures
		return redirect(self.view_name, **kwargs)

	def download_pictures(self, request, *args, **kwargs):
		if not request.POST['content'].strip():
			return redirect(self.view_name, **kwargs)
			
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

			return redirect(self.view_name, **kwargs)
		return self.render(request, form, kwargs.get('album_id', None))


class LibraryView(LoginRequiredMixin, BaseView):
	title = 'Bibliothèque - ' + TITLE
	template_name = 'gallery/library.html'
	view_name = 'gallery:library'

	def get(self, request, *args, **kwargs):
		albums = Album.objects.filter(user=request.user)

		context = self.get_base_context()
		context['albums'] = albums

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		actions = {
			'add': self.add_albums,
			'delete': self.delete_albums,
			'share': self.share_albums,
			'download': self.download_albums,
			'upload': self.upload_albums
		}

		default_fct = lambda r, *a, **k: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request, *args, **kwargs)

	def loop_albums_from_request(self, request):
		for pk in request.POST.get('content', '').strip().split(','):
			if pk.isdigit():
				pk = int(float(pk))
				album = get_object_or_404(Album, pk=pk, user=request.user)
				yield album

	def add_albums(self, request, *args, **kwargs):
		album_name = request.POST.get('content', '').strip()
		filters = {
			'user':request.user, 
			'category':'U', 
			'name': album_name
		}

		if Album.objects.filter(**filters).exists():
			return redirect(self.view_name)
		album = get_or_create_album(**filters)

		return redirect(AlbumView.view_name, album_id=album.id)

	def delete_albums(self, request, *args, **kwargs):
		for album in self.loop_albums_from_request(request):
			if album.category == 'U':
				album.delete()
		return redirect(self.view_name)

	def share_albums(self, request, *args, **kwargs):
		for album in self.loop_albums_from_request(request):
			pass
			# TODO: find a way to share albums
		return redirect(self.view_name)

	def download_albums(self, request, *args, **kwargs):
		if not request.POST['content'].strip():
			return redirect(self.view_name, **kwargs)
			
		zippath = settings.TMP_ROOT / 'zipfiles' / (get_illegible_name() + '.zip')
		filepaths = set()

		with zipfile.ZipFile(zippath, 'w', compression=zipfile.ZIP_DEFLATED) as file:
			for album in self.loop_albums_from_request(request):
				parent_dir = album.get_category_display() + ' - ' + album.name

				for picture in album.pictures.all():
					filepath = os.path.join(parent_dir, picture.filename)
				
					if filepath in filepaths:
						name, ext = os.path.splitext(filepath)
						filepath = name + ' ({})' + ext
						index = 2

						while filepath.format(index) in filepaths:
							index += 1
						filepath = filepath.format(index)
					filepaths.add(filepath)
					file.write(picture.image.path, arcname=filepath)
		
		return FileResponse(open(zippath, 'rb'), as_attachment=True, filename='Photos.zip')

	def upload_albums(self, request, *args, **kwargs):
		return redirect(self.view_name)


class SearchView(LoginRequiredMixin, BaseView):
	title = 'Recherche - ' + TITLE
	template_name = 'gallery/search.html'
	view_name = 'gallery:search'

	def get(self, request, *args, **kwargs):
		question = request.GET.get('query')
		pictures = []

		if question:
			words = question.split()

			for word in words:
				pictures += list(Picture.objects.filter(user=request.user, tags__icontains=word))

		context = self.get_base_context()
		context['pictures'] = pictures

		return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, BaseView):
	title = 'Réglages - ' + TITLE
	template_name = 'gallery/settings.html'
	view_name = 'gallery:settings'


class RegisterView(BaseView):
	title = 'Créer un compte - ' + TITLE
	template_name = 'registration/register.html'
	view_name = 'gallery:register'
	logged = False

	def render(self, request, form):
		context = self.get_base_context()
		context['form'] = form

		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('gallery:gallery')
		return self.render(request, UserCreationForm())

	def post(self, request, *args, **kwargs):
		form = UserCreationForm(request.POST, error_class=ErrorList)

		if form.is_valid():
			user = form.save()
			login(request, user)

			return redirect('gallery:gallery')

		return self.render(request, form)