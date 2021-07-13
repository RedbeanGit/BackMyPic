#    This file is part of BackMyPic.

#    BackMyPic is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    BackMyPic is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with BackMyPic.  If not, see <https://www.gnu.org/licenses/>.

import os
import random

from datetime import datetime
from django.core.files.storage import default_storage
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from .utils import get_illegible_name, get_picture_date, get_picture_size


def get_picture_path(instance, filename):
	name = get_illegible_name() + os.path.splitext(filename)[-1]
	return 'pictures/user_{0}/{1}'.format(instance.user.id, name)


class Picture(models.Model):
	date = models.DateTimeField('date', default=datetime.now)
	image = models.ImageField(upload_to=get_picture_path)
	width = models.IntegerField(null=True)
	height = models.IntegerField(null=True)
	tags = models.CharField('tags', max_length=200, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	filename = models.CharField(max_length=200, default='Unknown')
	hidden = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'photo'
		ordering = ['-date']

	def __str__(self):
		return '(name=' + self.filename + ', user=' + str(self.user) + ', date=' + str(self.date) + ')'

	def save(self, force_insert=False, force_update=False):
		super(Picture, self).save(force_insert=force_insert, force_update=force_update)
		self.date = get_picture_date(self)
		self.width, self.height = get_picture_size(self)
		super(Picture, self).save(force_insert=force_insert, force_update=force_update)


class Album(models.Model):
	CATEGORIES = (
		('D', 'Dates'),
		('U', 'User'),
		('S', 'Special')
	)

	name = models.CharField('nom', max_length=200)
	date = models.DateTimeField('date', auto_now_add=True)
	category = models.CharField('categorie', max_length=1, choices=CATEGORIES, default='U')
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	pictures = models.ManyToManyField(Picture)

	class Meta:
		verbose_name = 'album'

	def __str__(self):
		return '(user=' + str(self.user) + ', name=' + str(self.name) + ')'


class UserSettings(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_settings')
	current_album = models.OneToOneField(Album, on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'réglage utilisateur'

	def __str__(self):
		return '(user=' + str(self.user) + ')'


@receiver(models.signals.post_delete, sender=Picture)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""
	Deletes file from filesystem
	when corresponding `MediaFile` object is deleted.
	"""
	if instance.image:
		if os.path.isfile(instance.image.path):
			os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Picture)
def auto_delete_file_on_change(sender, instance, **kwargs):
	"""
	Deletes old file from filesystem
	when corresponding `MediaFile` object is updated
	with new file.
	"""
	if not instance.pk:
		return False

	try:
		old_file = Picture.objects.get(pk=instance.pk).image
	except Picture.DoesNotExist:
		return False

	new_file = instance.image
	if not old_file == new_file:
		if os.path.isfile(old_file.path):
			os.remove(old_file.path)