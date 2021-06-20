import calendar
import datetime
import piexif
import random
import unidecode

from os import path as op
from PIL import Image


def get_illegible_name(size=32):
	CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	return ''.join(random.choice(CHARS) for _ in range(size))


def get_picture_metadata(picture):
	try:
		with Image.open(picture.image.path) as image:
			return piexif.load(image.info['exif'])
	except Exception:
		return {}


def get_picture_date(picture):
	exifs = get_picture_metadata(picture).get('Exif', {})
	raw_datetime = ''
	date = datetime.datetime.fromtimestamp(op.getmtime(picture.image.path))
	codes = (36867, 36868, 306)

	for code in codes:
		try:
			raw_datetime = exifs.get(code).decode()
		except Exception:
			pass
		else:
			break
	try:
		date = datetime.datetime.strptime(raw_datetime, "%Y:%m:%d %H:%M:%S")
	except Exception:
		pass
	return date


def get_picture_size(picture):
	metadata = get_picture_metadata(picture)
	w, h = picture.image.width, picture.image.height
	orientation = metadata.get('0th', {}).get(274, 1)
	transformation = metadata.get('Exif', {}).get(48130, 1)
	
	if orientation > 4:
		w, h = h, w
	if transformation >= 4:
		w, h = h, w

	return w, h


def translate_month(name):
	MONTH_FR = ('janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre')
	month = unidecode.unidecode(name).lower()

	if month in MONTH_FR:
		return str(MONTH_FR.index(month) + 1)
	if month.capitalize() in calendar.month_name:
		return str(calendar.month_name.index(month.capitalize()))
	return None