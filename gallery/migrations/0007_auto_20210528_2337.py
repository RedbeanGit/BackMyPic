# Generated by Django 3.1.4 on 2021-05-28 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20210528_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='width',
            field=models.IntegerField(null=True),
        ),
    ]
