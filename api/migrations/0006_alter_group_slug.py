# Generated by Django 3.2.3 on 2021-05-30 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210530_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(null=True, unique=True, verbose_name='Ключ для создания URL'),
        ),
    ]