# Generated by Django 2.2.3 on 2019-09-17 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0022_transferinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferinfo',
            name='payee_real_name',
            field=models.CharField(default=None, max_length=100, verbose_name='收款方姓名'),
        ),
    ]
