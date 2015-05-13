# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectmgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('steps', models.TextField()),
                ('expected_result', models.TextField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Created')),
                ('is_automated', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'NE', max_length=10)),
                ('category', models.ForeignKey(to='projectmgmt.Category')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='projectmgmt.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestcaseHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('steps', models.TextField()),
                ('expected_result', models.TextField()),
                ('is_automated', models.BooleanField()),
                ('modified_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date Modified')),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='projectmgmt.Project')),
                ('testcase', models.ForeignKey(to='testcasemgmt.TestCase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
