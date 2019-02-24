# Generated by Django 2.1.5 on 2019-01-31 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cfd', '0008_auto_20190131_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfd',
            name='CLIENT_NAME',
        ),
        migrations.RemoveField(
            model_name='cfd',
            name='REMEDY_CLIENT_ID',
        ),
        migrations.AddField(
            model_name='cfd',
            name='CLIENT',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='cfd.client'),
            preserve_default=False,
        ),
    ]