# Generated by Django 4.1.1 on 2022-09-20 22:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]