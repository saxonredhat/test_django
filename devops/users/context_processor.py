from .models import Menu

def topmenus(request):
	topmenus = Menu.objects.filter(is_topmenu=True)
	return {'topmenus': topmenus}
