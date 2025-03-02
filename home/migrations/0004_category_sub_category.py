# Generated by Django 4.2.13 on 2024-05-22 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_products_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="sub_category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subcategories",
                to="home.category",
            ),
        ),
    ]
