# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-26 17:38
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TipoEstudio', models.CharField(max_length=200)),
                ('Fecha_creacion', models.DateField(auto_now=True)),
                ('Campo', models.TextField()),
                ('Conclusion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MedicoSolicitante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=128)),
                ('Apellido', models.CharField(max_length=128)),
                ('Telefono', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('Fecha', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cedula', models.IntegerField(error_messages={'unique': 'Ya existe un paciente con esta cédula en el sistema'}, unique=True)),
                ('Nombre', models.CharField(max_length=128)),
                ('Apellido', models.CharField(max_length=128)),
                ('Telefono', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999999999)])),
                ('Fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('Fecha_ingreso', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Diagnostico_presuntivo', models.CharField(blank=True, max_length=255, null=True)),
                ('Fecha_pedido', models.DateField(auto_now=True)),
                ('Fecha', models.DateField(auto_now=True)),
                ('Cortecia', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('Medico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.MedicoSolicitante')),
                ('Paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Placa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(blank=True, choices=[('AGFA 8 X 10', 'AGFA 8 X 10'), ('AGFA 10 X 14', 'AGFA 10 X 14'), ('AGFA 14 X 17', 'AGFA 14 X 17'), ('FUJI 8 X 10', ' FUJI 8 X 10'), ('FUJI 10 X 14', 'FUJI 10 X 14'), ('FUJI 14 X 17', 'FUJI 14 X 17')], max_length=255, null=True)),
                ('Fecha', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plantilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fecha_creacion', models.DateField(auto_now=True)),
                ('Campo', models.TextField()),
                ('Conclusion', models.CharField(max_length=200)),
                ('NombreDoc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='TipoEstudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('Fecha_creacion', models.DateField(auto_now=True)),
                ('Plantilla', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Plantilla')),
                ('Subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Subcategoria')),
            ],
        ),
        migrations.AddField(
            model_name='historia',
            name='Pedido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='hcapp.Pedido'),
        ),
    ]
