# Generated by Django 4.2.11 on 2024-05-02 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0002_remove_book_image_remove_book_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1234, upload_to='book_media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='quantity',
            field=models.IntegerField(default=''),
            preserve_default=False,
        ),
    ]
