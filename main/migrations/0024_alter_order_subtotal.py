# Generated by Django 4.1.6 on 2023-02-24 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_cart_razorpay_order_id_cart_razorpay_payment_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="subtotal",
            field=models.PositiveIntegerField(null=True),
        ),
    ]