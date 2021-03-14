import datetime
import piexif
import random

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