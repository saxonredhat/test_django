# Generated by Django 2.1.7 on 2019-04-06 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190406_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='link_name',
            field=models.CharField(blank=True, max_length=80, unique=True, verbose_name='link_name'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='parent_menu',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='submenus', to='users.Menu'),
        ),
    ]