# Generated by Django 2.1.7 on 2019-04-09 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_auto_20190409_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assets',
            name='assets_group',
            field=models.ManyToManyField(blank=True, null=True, to='assets.AssetsGroup', verbose_name='资产组'),
        ),
    ]
