# Generated by Django 4.0.6 on 2022-08-17 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0010_stock_last_table_date_stock_second_table_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='isin',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]