# Generated by Django 2.2 on 2020-11-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201101_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='browser_finger',
            field=models.CharField(blank=True, max_length=225, null=True, verbose_name='Browser finger print'),
        ),
    ]
