# Generated by Django 3.2.5 on 2021-07-31 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_dispatcher', '0003_onetimepasscodesms_verfied_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepasscodesms',
            name='verified',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]