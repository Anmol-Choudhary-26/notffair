# Generated by Django 4.0.1 on 2022-11-01 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='chater1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chater1', to=settings.AUTH_USER_MODEL),
        ),
    ]
