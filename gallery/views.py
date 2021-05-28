import datetime
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
from django.db.models import CharField, QuerySet
from django.db.models.functions import Lower
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic.base import View

from .forms import ErrorList, PictureForm
from .models import Picture, Album, UserSettings
from .utils import get_illegible_name, translate_month

CharField.register_lookup(Lower)

VERSION = '0.7.0'
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


def get_album_from_id(user, album_id=None):
	if album_id is None:
		user_settings = get_or_create_user_settings(user)
		album = user_settings.current_album
	else:
		album = get_object_or_404(Album, pk=album_id, user=user)
	return album


class BaseView(View):
	title = TITLE
	version = VERSION
	template_name = 'gallery/base.html'
	view_name = 'gallery:gallery'
	nav_bar = True
	nav_selected = ()
	action_elements = ()
	action_search_view = view_name

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.get_base_context())

	def get_base_context(self):
		return {
			'title': self.title,
			'version': self.version,
			'viewName': self.view_name,
			'navBar': self.nav_bar,
			'navSelected': self.nav_selected,
			'actionElements': self.action_elements,
			'actionSearchView': self.action_search_view
		}


class LibraryView(LoginRequiredMixin, BaseView):
	title = 'Bibliothèque - ' + TITLE
	template_name = 'gallery/library.html'
	view_name = 'gallery:library'
	nav_selected = ('library',)
	action_elements = ('select', 'download', 'add', 'delete', 'share')
	action_search_view = view_name

	def get(self, request):
		question = request.GET.get('query', None)

		if question is not None:
			context['previousSearch'] = question
			albums = Album.objects.filter(user=request.user, name__icontains=question).exclude(category='S', name='Search')
		else:
			albums = Album.objects.filter(user=request.user).exclude(category='S', name='search')
		
		context = self.get_base_context()
		context['albums'] = albums

		return render(request, self.template_name, context)

	def post(self, request):
		actions = {
			'upload': self.upload_albums,
			'download': self.download_albums,
			'add': self.add_albums,
			'delete': self.delete_albums,
			'share': self.share_albums
		}

		default_fct = lambda r: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request)

	def loop_albums_from_request(self, request):
		for pk in request.POST.get('content', '').strip().split(','):
			if pk.isdigit():
				pk = int(float(pk))
				album = get_object_or_404(Album, pk=pk, user=request.user)
				yield album

	def upload_albums(self, request):
		return redirect(self.view_name)

	def download_albums(self, request):
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

	def add_albums(self, request):
		album_name = request.POST.get('content', '').strip()
		filters = {
			'user': request.user,
			'category': 'U',
			'name': album_name
		}

		if Album.objects.filter(**filters).exists():
			return redirect(self.view_name)
		album = get_or_create_album(**filters)

		return redirect(AlbumView.view_name, album_id=album.id)

	def delete_albums(self, request):
		for album in self.loop_albums_from_request(request):
			if album.category == 'U':
				album.delete()
		return redirect(self.view_name)

	def share_albums(self, request):
		for album in self.loop_albums_from_request(request):
			pass
			# TODO: find a way to share albums
		return redirect(self.view_name)


class AlbumView(LoginRequiredMixin, BaseView):
	title = 'Album - ' + TITLE
	template_name = 'gallery/album.html'
	view_name = 'gallery:album'
	nav_selected = ('album',)
	action_elements = ('select', 'upload', 'download', 'delete', 'share', 'hide')
	action_search_view = view_name

	def render(self, request, form, album_id, page_id):

		context = self.get_base_context()
		context['form'] = form
		context['album'] = album

		return render(request, self.template_name, context)

	def search_for_date(self, question, pictures):
		patterns = (
			{
				'regex': r'(\s|^)[0-9]{1,2} [a-zA-Z]+ [0-9]{4}(\s|$)',
				'precision': 'day',
				'letter_month': True
			},
			{
				'regex': r'(\s|^)[0-9]{1,2}[\s/][0-9]{1,2}[\s/][0-9]{4}(\s|$)',
				'precision': 'day',
				'letter_month': False
			},
			{
				'regex': r'(\s|^)[a-zA-Z]+ [0-9]{4}(\s|$)',
				'precision': 'month',
				'letter_month': True
			},
			{
				'regex': r'(\s|^)[0-9]{1,2}[\s/][0-9]{4}(\s|$)',
				'precision': 'month',
				'letter_month': False
			},
			{
				'regex': r'(\s|^)[0-9]{4}(\s|$)',
				'precision': 'year',
				'letter_month': False
			}
		)

		for pattern in patterns:
			match = re.search(pattern['regex'], question)

			if match:
				a, b = match.span()
				datestr = question[a:b].replace('/', ' ').strip()

				if pattern['precision'] == 'day':
					day, month, year = datestr.split()

					if pattern['letter_month']:
						month = translate_month(month)

					date = datetime.datetime.strptime(day + ' ' + month + ' ' + year, '%d %m %Y')
					pictures = pictures.filter(date__year=date.year, date__month=date.month, date__day=date.day)
				elif pattern['precision'] == 'month':
					month, year = datestr.split()

					if pattern['letter_month']:
						month = translate_month(month)

					date = datetime.datetime.strptime(month + ' ' + year, '%m %Y')
					pictures = pictures.filter(date__year=date.year, date__month=date.month)
				else:
					year = datestr

					date = datetime.datetime.strptime(year, '%Y')
					pictures = pictures.filter(date__year=date.year)

				question = question.replace(question[a:b], '')
				break

		return pictures, question

	def search_for_size(self, question, pictures):
		rsize = r'(\s|^)[0-9]+x[0-9]+(\s|$)'
		match = re.search(rsize, question)

		if match:
			a, b = match.span()
			width, height = question[a:b].split('x')
			question = question.replace(question[a:b], '')

			return pictures.filter(width=int(width), height=int(height)), question
		return pictures, question

	def search_for_tags(self, question, pictures):
		words = question.split()
		
		for word in words:
			if word:
				pictures = pictures.intersection(Picture.objects.filter(tags__unaccent__icontains=word))
		return pictures, question

	def get(self, request, album_id=None, page_id=0):
		album = get_album_from_id(request.user, album_id)
		question = request.GET.get('query', None)
		context = self.get_base_context()
		context['form'] = PictureForm()
		
		if question:
			pictures = album.pictures.all()
			psize, question = self.search_for_size(question, pictures)
			pdate, question = self.search_for_date(question, pictures)
			ptags, question = self.search_for_tags(question, pictures)

			pictures = pdate.intersection(psize, ptags)
			album = get_or_create_album(user=request.user, name='search', category='S')
			album.pictures.all().delete()

			for picture in pictures:
				album.pictures.add(picture)
			context['previousSearch'] = question
			
		context['album'] = album
		return render(request, self.template_name, context)

	def post(self, request, album_id=None, page_id=0):
		actions = {
			'upload': self.upload_pictures,
			'download': self.download_pictures,
			'delete': self.delete_pictures,
			'share': self.share_pictures,
			'hide': self.hide_pictures
		}
		
		default_fct = lambda r, *a, **k: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request, album_id, page_id)

	def loop_pictures_from_request(self, request):
		for pk in request.POST['content'].strip().split(','):
			if pk.isdigit():
				pk = int(float(pk))
				picture = get_object_or_404(Picture, pk=pk, user=request.user)
				yield picture

	def upload_pictures(self, request, album_id, page_id):
		form = PictureForm(request.POST, request.FILES)

		if form.is_valid():
			album_gallery = get_or_create_album(user=request.user, category='S', name='gallery')
			album_current = get_album_from_id(request.user, album_id)
			images = request.FILES.getlist('image')

			for image in images:
				picture = Picture(image=image, user=request.user, filename=image.name)
				picture.save()
				album_gallery.pictures.add(picture)

				if album_current.category != 'S':
					album_current.pictures.add(picture)

			album_gallery.save()

			if album_current.category == 'S':
				if album_current.name == 'search':
					album_id = album_gallery.id
					page_id = 0
			else:
				album_current.save()
			
		return redirect(self.view_name, album_id=album_id, page_id=page_id)
	
	def download_pictures(self, request, album_id, page_id):
		if not request.POST['content'].strip():
			return redirect(self.view_name, album_id=album_id, page_id=page_id)
			
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

	def delete_pictures(self, request, album_id, page_id):
		for picture in self.loop_pictures_from_request(request):
			picture.delete()
		return redirect(self.view_name, album_id=album_id, page_id=page_id)

	def share_pictures(self, request, album_id, page_id):
		for picture in self.loop_pictures_from_request(request):
			pass
			# TODO: find a way to share pictures
		return redirect(self.view_name, album_id=album_id, page_id=page_id)

	def hide_pictures(self, request, album_id, page_id):
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

		return redirect(self.view_name, album_id=album_id, page_id=page_id)


class PictureView(LoginRequiredMixin, BaseView):
	title = 'Photo - ' + TITLE
	template_name = 'gallery/picture.html'
	view_name = 'gallery:picture'
	nav_selected = ('album',)
	action_elements = ('download', 'delete', 'share', 'hide')
	action_search_view = AlbumView.view_name

	def get(self, request, album_id, page_id, picture_id):
		context = self.get_base_context()
		context['album_id'] = album_id
		context['page_id'] = page_id
		context['picture_id'] = picture_id
		context['picture'] = get_object_or_404(Picture, user=request.user, pk=picture_id)

		return render(request, self.template_name, context)

	def post(self, request, album_id, page_id, picture_id):
		actions = {
			'download': self.download_picture,
			'delete': self.delete_picture,
			'share': self.share_picture,
			'hide': self.hide_picture,
		}
		
		default_fct = lambda r, *a, **k: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request, album_id, page_id, picture_id)

	def download_picture(self, request, album_id, page_id, picture_id):
		picture = get_object_or_404(Picture, user=request.user, pk=picture_id)
		return FileResponse(open(picture.image.path, 'rb'), as_attachment=True, filename=picture.filename)

	def delete_picture(self, request, album_id, page_id, picture_id):
		picture = get_object_or_404(Picture, user=request.user, pk=picture_id)
		picture.delete()
		return redirect(AlbumView.view_name, album_id=album_id, page_id=page_id)

	def share_picture(self, request, album_id, page_id, picture_id):
		# TODO: find a way to share pictures
		return redirect(self.view_name, album_id=album_id, page_id=page_id, picture_id=picture_id)

	def hide_picture(self, request, album_id, page_id, picture_id):
		filters = {'user': request.user, 'category': 'S'}

		album_gallery = get_or_create_album(**filters, name='gallery')
		album_hidden = get_or_create_album(**filters, name='hidden')
		picture = get_object_or_404(Picture, user=request.user, pk=picture_id)

		if album_gallery.pictures.filter(pk=picture_id).exists():
			album_gallery.pictures.remove(picture)

		if not album_hidden.pictures.filter(pk=picture_id).exists():
			album_hidden.pictures.add(picture)

		return redirect(self.view_name, album_id=album_id, page_id=page_id, picture_id=picture_id)


class SettingsView(LoginRequiredMixin, BaseView):
	title = 'Réglages - ' + TITLE
	template_name = 'gallery/settings.html'
	view_name = 'gallery:settings'
	nav_selected = ('settings',)

	def post(self, request):
		actions = {
			'delete': self.delete,
			'logout': self.logout,
			'save': self.save
		}

		default_fct = lambda r: redirect(self.view_name)
		action = actions.get(request.POST.get('action', None), default_fct)
		return action(request)

	def delete(self, request):
		if request.user.check_password(request.POST.get('confirm_password', '')):
			Picture.objects.filter(user=request.user).delete()
			Album.objects.filter(user=request.user).delete()
			request.user.delete()

			return redirect('gallery:logout')
		return self.get(request)

	def logout(self, request):
		return redirect('gallery:logout')

	def save(self, request):
		if request.user.check_password(request.POST.get('confirm_password', '')):
			request.user.username = request.POST.get('username', request.user.username)
			password = request.POST.get('password', '')

			if password:
				request.user.set_password(password)
			request.user.save()

		return self.get(request)


class RegisterView(BaseView):
	title = 'Créer un compte - ' + TITLE
	template_name = 'registration/register.html'
	view_name = 'gallery:register'
	nav_bar = False

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