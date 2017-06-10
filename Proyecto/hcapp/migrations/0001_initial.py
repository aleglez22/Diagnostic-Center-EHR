# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Nombre', models.CharField(null=True, max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Subcategoria', models.CharField(null=True, max_length=255, blank=True)),
                ('Fecha_creacion', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicoSolicitante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Nombre', models.CharField(max_length=128)),
                ('Apellido', models.CharField(max_length=128)),
                ('Telefono', models.IntegerField(null=True, max_length=10, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Cedula', models.IntegerField(unique=True)),
                ('Nombre', models.CharField(max_length=128)),
                ('Apellido', models.CharField(max_length=128)),
                ('Telefono', models.IntegerField(null=True, max_length=10, blank=True)),
                ('Edad', models.IntegerField(null=True, max_length=3, blank=True)),
                ('Fecha_nacimiento', models.DateField(null=True, blank=True)),
                ('Fecha_ingreso', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Diagnostico_presuntivo', models.CharField(null=True, max_length=255, blank=True)),
                ('Fecha', models.DateField(auto_now=True)),
                ('Medico', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hcapp.MedicoSolicitante')),
                ('Paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hcapp.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Radiologo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Nombre', models.CharField(max_length=128)),
                ('Apellido', models.CharField(max_length=128)),
                ('Telefono', models.IntegerField(null=True, max_length=10, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('Nombre', models.CharField(null=True, max_length=255, blank=True)),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hcapp.Categoria')),
            ],
        ),
    ]
