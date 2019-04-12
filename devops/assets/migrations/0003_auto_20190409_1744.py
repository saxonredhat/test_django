# Generated by Django 2.1.7 on 2019-04-09 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0002_auto_20190409_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='资产组名')),
                ('comment', models.CharField(max_length=100, unique=True, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='硬盘名')),
                ('size', models.CharField(max_length=100, unique=True, verbose_name='硬盘总空间')),
                ('usage_size', models.CharField(max_length=100, unique=True, verbose_name='硬盘已使用空间')),
                ('comment', models.CharField(max_length=100, unique=True, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='接口名')),
                ('interface_type', models.CharField(choices=[('network_card', '网卡'), ('port', '端口')], default='server', max_length=100, verbose_name='接口类型')),
                ('comment', models.CharField(max_length=100, unique=True, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=60, unique=True, verbose_name='IP地址')),
                ('ip_type', models.CharField(choices=[('ipv4', 'IPV4地址'), ('ipv6', 'IPV6地址')], default='ipv4', max_length=100, verbose_name='ip地址类型')),
                ('prefixlen', models.SmallIntegerField(blank=True, null=True, verbose_name='前缀长度')),
                ('comment', models.CharField(max_length=100, unique=True, verbose_name='描述')),
                ('interface', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ipaddress', to='assets.Interface', verbose_name='接口')),
            ],
        ),
        migrations.CreateModel(
            name='Memeory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='内存名')),
                ('size', models.CharField(max_length=100, unique=True, verbose_name='硬盘总空间')),
                ('usage_size', models.CharField(max_length=100, unique=True, verbose_name='硬盘已使用空间')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_type', models.CharField(choices=[('physical_machine', '物理机'), ('virtual_machine', '虚拟机'), ('container', '容器')], default='virtual_machine', max_length=100, verbose_name='服务器类型')),
            ],
        ),
        migrations.CreateModel(
            name='UserAssetsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assets_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assets.AssetsGroup', verbose_name='资产组')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.RemoveField(
            model_name='assets',
            name='management_ip',
        ),
        migrations.RemoveField(
            model_name='assets',
            name='mark',
        ),
        migrations.RemoveField(
            model_name='keystore',
            name='random_base64',
        ),
        migrations.AddField(
            model_name='keystore',
            name='assets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Assets', verbose_name='资产'),
        ),
        migrations.AddField(
            model_name='keystore',
            name='encode_key',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='加密KEY'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='asset_type',
            field=models.CharField(choices=[('server', '服务器'), ('router', '路由器'), ('switch', '交换机'), ('firewall', '防火墙')], default='server', max_length=100, verbose_name='资产类型'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='assets',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='keystore',
            name='comment',
            field=models.CharField(max_length=300, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='keystore',
            name='encode_password',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='加密密码'),
        ),
        migrations.AlterField(
            model_name='keystore',
            name='encode_private_key',
            field=models.TextField(blank=True, null=True, verbose_name='加密私钥'),
        ),
        migrations.AlterField(
            model_name='keystore',
            name='encode_public_key',
            field=models.TextField(blank=True, null=True, verbose_name='加密公钥'),
        ),
        migrations.AddField(
            model_name='server',
            name='assets',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assets.Assets', verbose_name='资产'),
        ),
        migrations.AddField(
            model_name='memeory',
            name='assets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memories', to='assets.Assets', verbose_name='资产'),
        ),
        migrations.AddField(
            model_name='interface',
            name='assets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='assets.Assets', verbose_name='资产'),
        ),
        migrations.AddField(
            model_name='disk',
            name='assets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disks', to='assets.Assets', verbose_name='资产'),
        ),
        migrations.AddField(
            model_name='assets',
            name='assets_group',
            field=models.ManyToManyField(to='assets.AssetsGroup', verbose_name='资产组'),
        ),
        migrations.AlterUniqueTogether(
            name='userassetsgroup',
            unique_together={('user', 'assets_group')},
        ),
    ]
