# Generated by Django 4.1.1 on 2022-09-21 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_alter_client_modified_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='auth2_country',
        ),
    ]
