# Generated by Django 2.2.3 on 2019-11-29 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0029_auto_20191121_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUpdateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('ios', 'ios'), ('android', 'android')], max_length=50, verbose_name='来源')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('version', models.CharField(max_length=100, verbose_name='版本')),
                ('is_force', models.BooleanField(verbose_name='是否强制')),
                ('describe', models.TextField(verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db.LocalStorage')),
            ],
        ),
    ]
