# Generated by Django 5.1.3 on 2024-12-02 09:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, help_text='Beschreibung der Kategorie', null=True)),
            ],
            options={
                'verbose_name': 'Kategorie',
                'verbose_name_plural': 'Kategorien',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, help_text='Beschreibung des Events', null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date', models.DateTimeField()),
                ('min_group', models.IntegerField(choices=[(10, 'mittelgroße Gruppe'), (2, 'sehr kleine Gruppe'), (20, 'große Gruppe')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category')),
            ],
        ),
    ]
