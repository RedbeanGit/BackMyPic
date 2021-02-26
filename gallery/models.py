import os
import random

from datetime import datetime
from django.core.files.storage import default_storage
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from .utils import get_illegible_name


def get_picture_path(instance, filename):
	name = get_illegible_name() + os.path.splitext(filename)[-1]
	return 'pictures/user_{0}/{1}'.format(instance.user.id, name)


class Picture(models.Model):
	date = models.DateTimeField('date', default=datetime.now)
	image = models.ImageField(upload_to=get_picture_path)
	tags = models.CharField('tags', max_length=200, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	filename = models.CharField(max_length=200, default='Unknown')
	hidden = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'photo'
		ordering = ['-date']

	def __str__(self):
		return str(self.user) + ' - ' + str(self.date)


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