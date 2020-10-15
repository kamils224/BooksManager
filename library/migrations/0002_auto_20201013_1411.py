# Generated by Django 3.1.2 on 2020-10-13 14:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=100, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_url',
            field=models.URLField(verbose_name='Cover'),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.CharField(max_length=13, validators=[django.core.validators.int_list_validator], verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(max_length=50, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(verbose_name='Pages'),
        ),
        migrations.AlterField(
            model_name='book',
            name='release_date',
            field=models.DateField(verbose_name='Release date'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
    ]
