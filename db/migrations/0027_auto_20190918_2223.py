# Generated by Django 2.2.3 on 2019-09-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0026_auto_20190918_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferinfo',
            name='status',
            field=models.CharField(max_length=64, verbose_name='支付状态'),
        ),
    ]
