from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserLoginForm, UserSigninForm, ErrorList
from .models import Picture, User


def index(request):
	pictures = Picture.objects.all().order_by('-date')[:12]
	context = {
		'pictures': pictures,
		'title': 'BackMyPic',
		'pic_count': pictures.count(),
		'col_len': 5,
		'search': True
	}

	return render(request, 'gallery/index.html', context)


def search(request):
	question = request.GET.get('query')
	pictures = []

	if question:
		words = question.split()

		for word in words:
			pictures += list(Picture.objects.filter(tags__icontains=word))

	context = {
		'pictures': pictures,
		'title': 'BackMyPic',
		'pic_count': len(pictures),
		'col_len': 5,
		'search': True
	}

	return render(request, 'gallery/index.html', context)


def settings(request):
	context = {
		'title': 'Paramètres - BackMyPic',
		'search': False
	}

	return render(request, 'gallery/settings.html', context)


def login(request):
	# si on appel cette vue avec POST, c'est qu'on a déjà rempli le formulaire
	if request.method == 'POST':
		form = UserLoginForm(request.POST, error_class=ErrorList)

		if form.is_valid():
			return redirect('gallery:gallery')
		else:
			errors = form.errors.items()
	# sinon c'est qu'on l'appelle pour la première fois
	else:
		form = UserLoginForm(error_class=ErrorList)
		errors = {}.items()

	context = {
		'title': 'Se connecter - BackMyPic',
		'errors': errors,
		'form': form,
		'search': False
	}

	return render(request, 'gallery/login.html', context)


def signin(request):
	# si on appel cette vue avec POST, c'est qu'on a déjà rempli le formulaire
	if request.method == 'POST':
		form = UserSigninForm(request.POST, error_class=ErrorList)

		if form.is_valid():
			return redirect('gallery:gallery')
		else:
			errors = form.errors.items()
	# sinon c'est qu'on l'appelle pour la première fois
	else:
		form = UserSigninForm(error_class=ErrorList)
		errors = {}.items()

	context = {
		'title': 'Créer un compte - BackMyPic',
		'errors': errors,
		'form': form,
		'search': False
	}

	return render(request, 'gallery/signin.html', context)