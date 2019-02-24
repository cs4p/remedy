# Generated by Django 2.1.5 on 2019-02-17 20:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfd', '0012_auto_20190206_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cfd',
            name='BRAND_RETAIL_90_RETAIL_AT_MAIL_RATES',
        ),
        migrations.RemoveField(
            model_name='cfd',
            name='GENERIC_RETAIL_90_RETAIL_AT_MAIL_RATES',
        ),
        migrations.AddField(
            model_name='cfd',
            name='RETAIL_90_MAIL_RATES_B',
            field=models.CharField(choices=[('Y - Retail-90', 'Y - Retail-90'), ('Y - Retail at Mail Rates', 'Y - Retail at Mail Rates'), ('Y - Retail-90 & Retail at Mail Rates', 'Y - Retail-90 & Retail at Mail Rates'), ('N', 'N')], default='N', max_length=50, verbose_name='Brand Retail-90/Retail at Mail Rates'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cfd',
            name='RETAIL_90_MAIL_RATES_G',
            field=models.CharField(choices=[('Y - Retail-90', 'Y - Retail-90'), ('Y - Retail at Mail Rates', 'Y - Retail at Mail Rates'), ('Y - Retail-90 & Retail at Mail Rates', 'Y - Retail-90 & Retail at Mail Rates'), ('N', 'N')], default='N', max_length=50, verbose_name='Generic Retail-90/Retail at Mail Rates'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cfd',
            name='END_DATE',
            field=models.DateField(default=datetime.date(2020, 2, 17), verbose_name='Contract End Date'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='GUAR_BR90_DISP_FEE',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Retail-90 Brand Dispensing Fee'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='GUAR_BR_DISP_FEE',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Retail Brand Dispensing Fee'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='GUAR_GR90_DISP_FEE',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Retail-90 Generic Dispensing Fee'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='GUAR_GR_DISP_FEE',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6, verbose_name='Retail Generic Dispensing Fee'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='RETAIL_90_MAIL_RATES_G_DS',
            field=models.IntegerField(default=0, verbose_name='Retail-90/Retail at Mail Rates Generic Days Supply Breakout'),
        ),
        migrations.AlterField(
            model_name='cfd',
            name='START_DATE',
            field=models.DateField(default=datetime.date(2019, 2, 17), verbose_name='Contract Start Date'),
        ),
    ]