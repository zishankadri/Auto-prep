# Generated by Django 4.2.7 on 2024-01-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_subchapter_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subchapter',
            name='number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
