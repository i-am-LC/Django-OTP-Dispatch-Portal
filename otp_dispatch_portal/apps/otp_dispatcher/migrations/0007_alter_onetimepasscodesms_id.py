# Generated by Django 4.1.1 on 2022-09-20 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otp_dispatcher', '0006_alter_onetimepasscodesms_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepasscodesms',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]