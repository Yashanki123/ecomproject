# Generated by Django 4.1.6 on 2023-02-17 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_remove_customer_mobile"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="mobile",),
        migrations.AddField(
            model_name="order",
            name="change_address",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
