# Generated by Django 3.0.6 on 2020-06-22 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200622_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 159000)),
        ),
        migrations.AlterField(
            model_name='banner',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 159000)),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 150001)),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 151000)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 152001)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 152001)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 154001)),
        ),
        migrations.AlterField(
            model_name='menu',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 154001)),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 156001)),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 156001)),
        ),
        migrations.AlterField(
            model_name='order_detail',
            name='quantity',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 157000)),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 157000)),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 154999)),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 154999)),
        ),
        migrations.AlterField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 153001)),
        ),
        migrations.AlterField(
            model_name='topic',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 22, 16, 27, 20, 153001)),
        ),
    ]
