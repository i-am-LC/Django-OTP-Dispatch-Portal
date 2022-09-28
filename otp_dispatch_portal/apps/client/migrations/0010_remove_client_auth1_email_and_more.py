# Generated by Django 4.1.1 on 2022-09-26 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0009_alter_client_auth2_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='auth1_email',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth1_firstname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth1_mobile',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth1_surname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth2_email',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth2_firstname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth2_mobile',
        ),
        migrations.RemoveField(
            model_name='client',
            name='auth2_surname',
        ),
        migrations.RemoveField(
            model_name='client',
            name='country',
        ),
        migrations.AlterField(
            model_name='client',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='client',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='client_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='AuthorisedRepresentative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=12)),
                ('firstname', models.CharField(max_length=254)),
                ('surname', models.CharField(max_length=254)),
                ('role', models.CharField(max_length=254)),
                ('country', models.CharField(max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='client.client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='auth_rep_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='auth_rep_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
