# Generated by Django 4.1.1 on 2022-09-20 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=254)),
                ('auth1_email', models.EmailField(max_length=254)),
                ('aut1_mobile', models.CharField(max_length=12)),
                ('auth1_firstname', models.CharField(max_length=254)),
                ('auth1_surname', models.CharField(max_length=254)),
                ('auth2_email', models.EmailField(max_length=254)),
                ('auth2_mobile', models.CharField(max_length=12)),
                ('auth2_firstname', models.CharField(max_length=254)),
                ('auth2_surname', models.CharField(max_length=254)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
