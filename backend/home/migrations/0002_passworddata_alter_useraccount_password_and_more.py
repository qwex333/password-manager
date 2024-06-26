# Generated by Django 5.0.6 on 2024-06-05 08:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30)),
                ('account', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('reg_time', models.TimeField(default=datetime.datetime(2024, 6, 5, 16, 8, 2, 609291), verbose_name='time registered')),
            ],
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='reg_time',
            field=models.TimeField(default=datetime.datetime(2024, 6, 5, 16, 8, 2, 609291), verbose_name='time registered'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_name',
            field=models.CharField(max_length=30),
        ),
    ]
