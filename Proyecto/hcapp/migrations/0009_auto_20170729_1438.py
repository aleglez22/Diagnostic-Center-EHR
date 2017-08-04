# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-29 19:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hcapp', '0008_remove_paciente_edad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historia',
            name='Pedido',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='hcapp.Pedido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='Medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.MedicoSolicitante'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='Paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Paciente'),
        ),
        migrations.AlterField(
            model_name='subcategoria',
            name='Categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Categoria'),
        ),
        migrations.AlterField(
            model_name='tipoestudio',
            name='Subcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hcapp.Subcategoria'),
        ),
    ]
