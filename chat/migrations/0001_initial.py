# Generated by Django 4.0.1 on 2022-11-12 16:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nickname1', models.CharField(default='NoName1', max_length=100)),
                ('nickname2', models.CharField(default='Noname2', max_length=100)),
                ('roomBlocked', models.BooleanField(default=False, verbose_name='RoomBlocked')),
                ('chater1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chater1', to=settings.AUTH_USER_MODEL)),
                ('chater2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chater2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('reported', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter_user', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.room')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1000000)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.room')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
