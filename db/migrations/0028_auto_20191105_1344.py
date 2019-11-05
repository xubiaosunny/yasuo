# Generated by Django 2.2.3 on 2019-11-05 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0027_auto_20190918_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='workscomment',
            name='text',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='workscomment',
            name='type',
            field=models.CharField(choices=[('text', '文本'), ('voice', '语音')], default='voice', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worksquestionreply',
            name='text',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='worksquestionreply',
            name='type',
            field=models.CharField(choices=[('text', '文本'), ('voice', '语音')], default='voice', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workscomment',
            name='voice',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='db.LocalStorage'),
        ),
        migrations.AlterField(
            model_name='worksquestionreply',
            name='voice',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='db.LocalStorage'),
        ),
    ]
