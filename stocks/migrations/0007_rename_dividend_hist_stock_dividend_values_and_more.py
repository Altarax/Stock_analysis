# Generated by Django 4.0.6 on 2022-08-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_stock_capitalization_values_stock_debt_values_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='dividend_hist',
            new_name='dividend_values',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='stock_hist',
            new_name='stock_values',
        ),
        migrations.AddField(
            model_name='stock',
            name='bpr_values',
            field=models.TextField(null=True),
        ),
    ]
