# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectmgmt', '0001_initial'),
        ('testcasemgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('result', models.CharField(default=b'NE', max_length=10)),
                ('bugid', models.IntegerField(default=0)),
                ('comment', models.TextField(default=b'')),
                ('modified_date', models.DateField(auto_now_add=True, verbose_name=b'Date')),
                ('executed_by', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExecutionTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date')),
                ('status', models.IntegerField(default=0)),
                ('browsers', models.CharField(max_length=200, null=True, blank=True)),
                ('allocated_by', models.ForeignKey(related_name='executiontask_allocated_by', to=settings.AUTH_USER_MODEL)),
                ('allocated_to', models.ForeignKey(related_name='executiontask_allocated_to', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='projectmgmt.Category')),
                ('client_device', models.ForeignKey(to='projectmgmt.ClientDevice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date')),
                ('build', models.ForeignKey(to='projectmgmt.Build')),
                ('project', models.ForeignKey(to='projectmgmt.Project')),
                ('started_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='executiontask',
            name='testplan',
            field=models.ForeignKey(to='executionmgmt.TestPlan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='executionhistory',
            name='execution',
            field=models.ForeignKey(to='executionmgmt.ExecutionTask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='executionhistory',
            name='testcase',
            field=models.ForeignKey(to='testcasemgmt.TestCase'),
            preserve_default=True,
        ),
    ]
