# Generated by Django 2.1.7 on 2019-04-06 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190406_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='parent_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submenus', to='users.Menu'),
        ),
    ]
