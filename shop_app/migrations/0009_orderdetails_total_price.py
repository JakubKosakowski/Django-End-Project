# Generated by Django 4.2.1 on 2023-06-04 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0008_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
