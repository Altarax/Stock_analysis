# Generated by Django 4.0.6 on 2022-08-01 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_alter_stock_date_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='date_list',
            field=models.TextField(null=True),
        ),
    ]
