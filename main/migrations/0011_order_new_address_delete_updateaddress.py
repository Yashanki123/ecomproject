# Generated by Django 4.1.6 on 2023-02-21 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_cart_razor_pay_order_id_cart_razor_pay_payment_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="new_address",
            field=models.CharField(default=True, max_length=200),
        ),
        migrations.DeleteModel(name="UpdateAddress",),
    ]
