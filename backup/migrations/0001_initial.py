# Generated by Django 5.1.4 on 2024-12-16 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('github_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('github_url', models.URLField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repositories', to='backup.user')),
            ],
        ),
    ]
