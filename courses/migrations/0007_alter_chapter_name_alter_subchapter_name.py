# Generated by Django 4.2.7 on 2024-02-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_chapter_number_subchapter_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='subchapter',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
