import random


def get_illegible_name(size=32):
	CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	return ''.join(random.choice(CHARS) for _ in range(size))