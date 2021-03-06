# Generated by Django 2.2.2 on 2019-06-12 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_auto_20190610_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='db.LocalStorage'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='work_place',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='工作单位'),
        ),
    ]
