# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-01 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meal_plans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mealPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name=50)),
            ],
        ),
        migrations.DeleteModel(
            name='index',
        ),
    ]
