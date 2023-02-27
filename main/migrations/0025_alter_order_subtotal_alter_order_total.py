# Generated by Django 4.1.6 on 2023-02-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0024_alter_order_subtotal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="subtotal",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="total",
            field=models.PositiveIntegerField(verbose_name=True),
        ),
    ]
