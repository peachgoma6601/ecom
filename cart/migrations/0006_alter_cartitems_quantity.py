# Generated by Django 4.0.4 on 2022-05-24 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cartitems_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
