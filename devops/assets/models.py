from django.db import models
from users.models import User
from django.urls import reverse


# Create your models here.
class AssetsGroup(models.Model):
	name = models.CharField(max_length=100, unique=True, verbose_name='资产组名')
	comment = models.CharField(max_length=100, unique=True, verbose_name='描述')


class Assets(models.Model):
	ASSET_TYPE_CHOICES = (
		('server','服务器'),
		('router','路由器'),
		('switch','交换机'),
		('firewall','防火墙'),
	)
	asset_type = models.CharField(max_length=100,choices=ASSET_TYPE_CHOICES, default='server', verbose_name='资产类型')
	assets_group = models.ManyToManyField(AssetsGroup, blank=True, null=True, verbose_name='资产组') 
	name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name='资产编号')
	sn =  models.CharField(max_length=100, blank=True, null=True, verbose_name='设备序列号')
	buy_time = models.DateField(blank=True, null=True, verbose_name='购买时间')
	expire_date = models.DateField(null=True, blank=True, verbose_name='过保修期')
	manufacturer = models.CharField(max_length=100,blank=True, null=True, verbose_name='制造商')
	provider = models.CharField(max_length=100,blank=True, null=True, verbose_name='供货商')
	model = models.CharField(max_length=100,blank=True, null=True, verbose_name='资产型号')
	status = models.SmallIntegerField(blank=True, null=True, verbose_name='状态')
	put_zone = models.SmallIntegerField(blank=True, null=True, verbose_name='放置区域')
	group = models.SmallIntegerField(blank=True, null=True, verbose_name='使用组')
	business = models.SmallIntegerField(blank=True, null=True, verbose_name='业务类型')
	project = models.SmallIntegerField(blank=True, null=True, verbose_name='项目类型')
	cabinet = models.SmallIntegerField(blank=True, null=True, verbose_name='机柜位置')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
	updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
	
	def get_absolute_url(self):
		return reverse('assets:assets-list')



class Server(models.Model):
	SERVER_TYPE_CHOICES = (
		('physical_machine','物理机'),
		('virtual_machine','虚拟机'),
		('container','容器'),
	)
	assets = models.OneToOneField(Assets, on_delete=models.CASCADE, blank=True, null=True, verbose_name='资产')
	server_type = models.CharField(choices=SERVER_TYPE_CHOICES,max_length=100,default='virtual_machine', verbose_name='服务器类型')

class Interface(models.Model):
	INTERFACE_TYPE_CHOICES = (
		('network_card','网卡'),
		('port','端口'),
	)
	assets = models.ForeignKey(Assets, on_delete=models.CASCADE, blank=True, null=True, related_name='interfaces', verbose_name='资产')
	name = models.CharField(max_length=100, unique=True, verbose_name='接口名')
	interface_type = models.CharField(max_length=100, choices=INTERFACE_TYPE_CHOICES, default='server', verbose_name='接口类型')
	comment = models.CharField(max_length=100, unique=True, verbose_name='描述')


class IpAddress(models.Model):
	IP_TYPE_CHOICES = (
		('ipv4','IPV4地址'),
		('ipv6','IPV6地址'),
	)
	interface = models.ForeignKey(Interface, on_delete=models.CASCADE, blank=True, null=True,related_name='ipaddress', verbose_name='接口')
	ip = models.CharField(max_length=60, unique=True, verbose_name='IP地址')
	ip_type = models.CharField(choices=IP_TYPE_CHOICES,default='ipv4',max_length=100, verbose_name='ip地址类型')
	prefixlen = models.SmallIntegerField(blank=True, null=True, verbose_name='前缀长度')
	comment = models.CharField(max_length=100, unique=True, verbose_name='描述')
	

class Disk(models.Model):
	assets = models.ForeignKey(Assets, on_delete=models.CASCADE, blank=True, null=True, related_name='disks', verbose_name='资产')
	name = models.CharField(max_length=100, unique=True, verbose_name='硬盘名')
	size = models.CharField(max_length=100, unique=True, verbose_name='硬盘总空间')
	usage_size = models.CharField(max_length=100, unique=True, verbose_name='硬盘已使用空间')
	comment = models.CharField(max_length=100, unique=True, verbose_name='描述')

class Memeory(models.Model):
	assets = models.ForeignKey(Assets, on_delete=models.CASCADE, blank=True, null=True, related_name='memories', verbose_name='资产')
	name = models.CharField(max_length=100, unique=True, verbose_name='内存名')
	size = models.CharField(max_length=100, unique=True, verbose_name='硬盘总空间')
	usage_size = models.CharField(max_length=100, unique=True, verbose_name='硬盘已使用空间')
	

class KeyStore(models.Model):
	assets = models.ForeignKey(Assets, on_delete=models.CASCADE, blank=True, null=True, verbose_name='资产')
	encode_password = models.CharField(max_length=100, blank=True, null=True, verbose_name='加密密码')
	encode_private_key = models.TextField(blank=True, null=True, verbose_name='加密私钥')
	encode_public_key = models.TextField(blank=True, null=True, verbose_name='加密公钥')
	encode_key = models.CharField(max_length=200, blank=True, null=True, verbose_name='加密KEY')
	comment = models.CharField(max_length=300, verbose_name='描述')


class UserAssetsGroup(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
	assets_group = models.OneToOneField(AssetsGroup, on_delete=models.CASCADE, verbose_name='资产组')

	class Meta:
		unique_together = ('user', 'assets_group',)
