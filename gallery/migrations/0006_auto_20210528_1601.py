from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20210326_2241')
    ]

    operations = [
        UnaccentExtension()
    ]