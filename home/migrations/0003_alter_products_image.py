# Generated by Django 5.0.3 on 2024-05-21 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_alter_products_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="image",
            field=models.ImageField(
                default="product_images/no_image.jpg", upload_to="product_images/"
            ),
        ),
    ]
