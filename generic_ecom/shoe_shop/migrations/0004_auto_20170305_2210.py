# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoe_shop', '0003_auto_20170305_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='created',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='created',
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='created',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='inventorytype',
            name='modified_by',
        ),
    ]
