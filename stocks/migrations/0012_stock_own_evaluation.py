# Generated by Django 4.1 on 2022-09-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0011_stock_isin"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="own_evaluation",
            field=models.TextField(null=True),
        ),
    ]