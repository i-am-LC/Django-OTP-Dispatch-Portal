# Generated by Django 3.2.5 on 2021-08-01 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_dispatcher', '0005_rename_verfied_datetime_onetimepasscodesms_verified_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepasscodesms',
            name='mobile_number',
            field=models.CharField(max_length=12),
        ),
    ]
