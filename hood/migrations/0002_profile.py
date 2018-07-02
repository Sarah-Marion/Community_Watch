# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-01 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hood', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_confirmed', models.BooleanField(default=False)),
                ('idNumber', models.CharField(max_length=8, null=True, unique=True)),
                ('name', models.CharField(blank=True, max_length=500)),
                ('avatar', models.ImageField(upload_to='profilepic/')),
                ('generalLocation', models.TextField(blank=True, max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('hood', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hood.Hood')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
