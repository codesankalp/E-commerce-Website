# Generated by Django 3.1.3 on 2020-11-25 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200813_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-time']},
        ),
    ]