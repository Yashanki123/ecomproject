# Generated by Django 4.1.6 on 2023-02-20 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_remove_order_mobile_order_change_address"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="change_address",),
        migrations.CreateModel(
            name="UpdateAddress",
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
                ("shipping_address", models.CharField(max_length=200)),
                ("change_address", models.CharField(max_length=200)),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.customer",
                    ),
                ),
            ],
        ),
    ]
