# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-06 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklist', '0002_book_amazonurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='amazonURL',
            field=models.URLField(default=b'https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=', null=True),
        ),
    ]
