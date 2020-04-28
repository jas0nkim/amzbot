# Generated by Django 3.0.5 on 2020-04-28 04:51

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('project', models.CharField(db_index=True, max_length=32)),
                ('spider', models.CharField(db_index=True, max_length=32)),
                ('version', models.CharField(blank=True, max_length=32, null=True)),
                ('settings', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('other_params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.SmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'sched_jobs',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(db_index=True, max_length=32)),
                ('version', models.CharField(db_index=True, max_length=32)),
                ('status', models.SmallIntegerField(default=1)),
                ('added_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sched_versions',
                'unique_together': {('project', 'version')},
            },
        ),
    ]
