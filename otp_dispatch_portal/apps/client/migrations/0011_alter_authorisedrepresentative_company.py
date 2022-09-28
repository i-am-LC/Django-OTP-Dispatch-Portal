# Generated by Django 4.1.1 on 2022-09-27 01:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_remove_client_auth1_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorisedrepresentative',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='auth_rep_company', to='client.client'),
        ),
    ]
