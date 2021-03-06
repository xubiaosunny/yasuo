# Generated by Django 2.2.3 on 2019-08-07 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0019_auto_20190725_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, verbose_name='人员状态'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255, verbose_name='Message')),
                ('class_name', models.CharField(choices=[('Works', 'Works'), ('WorksQuestion', 'WorksQuestion'), ('CustomUser', 'CustomUser')], max_length=50)),
                ('class_id', models.IntegerField()),
                ('is_read', models.BooleanField(default=False)),
                ('push_time', models.DateTimeField(auto_now_add=True, verbose_name='Push Time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
