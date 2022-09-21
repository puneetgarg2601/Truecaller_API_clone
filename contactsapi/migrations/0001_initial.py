# Generated by Django 4.0.4 on 2022-06-05 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('email', models.EmailField(default='', max_length=100, verbose_name='Email')),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('spam_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('phone_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contactsapi.phonenumber', verbose_name='Number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='contact_user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no',
            field=models.OneToOneField(max_length=10, on_delete=django.db.models.deletion.PROTECT, to='contactsapi.phonenumber', verbose_name='phone'),
        ),
    ]
