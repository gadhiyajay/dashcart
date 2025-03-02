# Generated by Django 4.2.13 on 2024-05-22 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_category_sub_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(0, "Inactive"), (1, "Active")],
                        default=1,
                        verbose_name="status",
                    ),
                ),
                (
                    "activate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for an immediate activation",
                        null=True,
                    ),
                ),
                (
                    "deactivate_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="keep empty for indefinite activation",
                        null=True,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.PositiveIntegerField(default=50)),
                (
                    "image",
                    models.ImageField(
                        default="static/product_images/no_image.jpg",
                        upload_to="static/product_images/",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="subcategory",
            name="sub_category",
        ),
        migrations.AlterModelOptions(
            name="category",
            options={},
        ),
        migrations.AddField(
            model_name="category",
            name="category_image",
            field=models.ImageField(
                default="static/product_images/no_image.jpg",
                upload_to="static/product_images/",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="sub_category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="home.category",
            ),
        ),
        migrations.DeleteModel(
            name="Products",
        ),
        migrations.DeleteModel(
            name="SubCategory",
        ),
        migrations.AddField(
            model_name="product",
            name="categories",
            field=models.ManyToManyField(to="home.category"),
        ),
    ]
