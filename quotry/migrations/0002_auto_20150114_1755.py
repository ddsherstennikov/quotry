# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotry', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favs',
            field=models.ManyToManyField(to=b'quotry.Tag', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='likes',
            field=models.ManyToManyField(to=b'quotry.Quote', blank=True),
        ),
    ]
