# Generated by Django 4.2.13 on 2024-05-24 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_alter_category_image_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                default="static/images/no_image.jpg", upload_to="static/images/"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="static/images/no_image.jpg", upload_to="static/images/"
            ),
        ),
    ]
