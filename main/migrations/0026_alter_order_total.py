# Generated by Django 4.1.6 on 2023-02-24 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0025_alter_order_subtotal_alter_order_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total",
            field=models.PositiveIntegerField(null=True),
        ),
    ]