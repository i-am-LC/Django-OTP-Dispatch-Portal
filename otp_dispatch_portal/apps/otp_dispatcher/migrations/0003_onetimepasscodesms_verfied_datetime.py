# Generated by Django 3.2.5 on 2021-07-31 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_dispatcher', '0002_rename_region_onetimepasscodesms_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='onetimepasscodesms',
            name='verfied_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]