# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hcapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicosolicitante',
            name='Telefono',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Edad',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(200)], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='Telefono',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='radiologo',
            name='Telefono',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999999999)], blank=True, null=True),
        ),
    ]
