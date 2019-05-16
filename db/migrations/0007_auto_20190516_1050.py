# Generated by Django 2.2.1 on 2019-05-16 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20190514_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='certified_file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='db.LocalStorage'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='id_number',
            field=models.CharField(blank=True, max_length=100, verbose_name='身份证号'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='reject_cause',
            field=models.TextField(verbose_name='拒绝原因'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='status',
            field=models.CharField(choices=[('Verifying', '审核中'), ('Pass', '通过'), ('Reject', '拒绝')], max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='grade',
            field=models.IntegerField(blank=True, choices=[('10', '高一'), ('11', '高二'), ('12', '高三'), ('13', '复读')], null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=100, unique=True, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='province',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='省'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('T', '老师'), ('S', '学生')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='work_place',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='工作单位'),
        ),
        migrations.AlterField(
            model_name='smscode',
            name='code',
            field=models.CharField(max_length=20, verbose_name='短信验证码'),
        ),
    ]
