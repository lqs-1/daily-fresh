# Generated by Django 4.0.1 on 2022-01-21 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_orderinfo_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='order_id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单id'),
        ),
    ]
