# Generated by Django 3.0.6 on 2020-06-22 02:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200622_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_detail',
            name='price',
        ),
        migrations.AlterField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 168046)),
        ),
        migrations.AlterField(
            model_name='banner',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 168046)),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 163059)),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 163059)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 164050)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 164050)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 165049)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 165049)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 166052)),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 167049)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 168046)),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 168046)),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 166052)),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 166052)),
        ),
        migrations.AlterField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 164050)),
        ),
        migrations.AlterField(
            model_name='topic',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 9, 23, 11, 164050)),
        ),
    ]