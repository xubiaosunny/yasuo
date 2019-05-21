# Generated by Django 2.2.1 on 2019-05-18 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_auto_20190516_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='localstorage',
            name='watermarked_filename',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='watermarked filename'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='id_number',
            field=models.CharField(blank=True, max_length=100, verbose_name='ID Number'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='reject_cause',
            field=models.TextField(verbose_name='Reject Cause'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='status',
            field=models.CharField(choices=[('Verifying', 'Verifying'), ('Pass', 'Pass'), ('Reject', 'Reject')], max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='grade',
            field=models.IntegerField(blank=True, choices=[('10', 'grade ten'), ('11', 'grade eleven'), ('12', 'grade twelve'), ('13', 'return students')], null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=100, unique=True, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='province',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='province'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('T', 'Teacher'), ('S', 'Student')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='work_place',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Work Place'),
        ),
        migrations.AlterField(
            model_name='smscode',
            name='code',
            field=models.CharField(max_length=20, verbose_name='SMS Code'),
        ),
    ]