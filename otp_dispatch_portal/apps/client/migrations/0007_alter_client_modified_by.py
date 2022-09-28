# Generated by Django 4.1.1 on 2022-09-21 01:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0006_rename_auth1_country_client_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT, related_name='modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
