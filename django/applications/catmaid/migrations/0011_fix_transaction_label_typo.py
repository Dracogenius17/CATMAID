# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-17 19:09
from __future__ import unicode_literals

from django.db import migrations

forward = """
    UPDATE catmaid_transaction_info
    SET label = 'skeletons.merge'
    WHERE label = 'skeletonss.merge'
    """

backward = """
    UPDATE catmaid_transaction_info
    SET label = 'skeletonss.merge'
    WHERE label = 'skeletons.merge'
    """

class Migration(migrations.Migration):

    dependencies = [
        ('catmaid', '0010_history_tracking_update'),
    ]

    operations = [
        migrations.RunSQL(forward, backward)
    ]
