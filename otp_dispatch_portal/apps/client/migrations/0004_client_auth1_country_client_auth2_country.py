# Generated by Django 4.1.1 on 2022-09-20 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_client_modified_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='auth1_country',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='auth2_country',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
