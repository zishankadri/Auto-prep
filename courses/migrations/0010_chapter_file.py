# Generated by Django 4.2.7 on 2024-10-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_delete_subchapter'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='file',
            field=models.FileField(default='', upload_to='chapters/'),
            preserve_default=False,
        ),
    ]
