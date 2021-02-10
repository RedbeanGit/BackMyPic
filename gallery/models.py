from datetime import datetime
from django.db import models


class User(models.Model):
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=200)


class Picture(models.Model):
	date = models.DateTimeField(default=datetime.now)
	
	width = models.IntegerField(default=1)
	height = models.IntegerField(default=1)
	
	url = models.URLField(max_length=200)
	
	latitude = models.FloatField(default=0)
	longitude = models.FloatField(default=0)

	tags = models.CharField(max_length=200, null=True)
	
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)