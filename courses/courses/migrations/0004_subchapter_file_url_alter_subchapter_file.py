# Generated by Django 4.2.7 on 2024-01-27 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_subchapter_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='subchapter',
            name='file_url',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subchapter',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=''),
        ),
    ]