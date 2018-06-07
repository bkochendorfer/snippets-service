# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-21 09:34
from __future__ import unicode_literals

from django.db import migrations


def migrate_disabled_to_published(apps, schema_editor):
    Snippet = apps.get_model('base', 'Snippet')
    Snippet.objects.filter(disabled=False).update(published=True)
    Snippet.objects.filter(disabled=True).update(published=False)

    JSONSnippet = apps.get_model('base', 'Snippet')
    JSONSnippet.objects.filter(disabled=False).update(published=True)
    JSONSnippet.objects.filter(disabled=True).update(published=False)


def migrate_published_to_disabled(apps, schema_editor):
    Snippet = apps.get_model('base', 'Snippet')
    Snippet.objects.filter(published=False).update(disabled=True)
    Snippet.objects.filter(published=True).update(disabled=False)

    JSONSnippet = apps.get_model('base', 'Snippet')
    JSONSnippet.objects.filter(published=False).update(disabled=True)
    JSONSnippet.objects.filter(published=True).update(disabled=False)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_auto_20180521_0933'),
    ]

    operations = [
        migrations.RunPython(migrate_disabled_to_published, migrate_published_to_disabled)
    ]
