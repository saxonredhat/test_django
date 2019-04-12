from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView,FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.urls.exceptions import NoReverseMatch

from .models import Assets

from security.Cipher import AESCipher
from assets.models import KeyStore
import base64
import random
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Create your views here.


class AssetsListView(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    ListView):
    permission_required = 'ASSET_VIEW'
    model = Assets 


class AssetsCreateView(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    CreateView):
    permission_required = 'ASSET_ADD'
    model = Assets 
    fields = ['asset_type', 'assets_group', 'name', 'sn', 'buy_time', 'expire_date', 'manufacturer', 'provider', 'model', 'status', 'put_zone', 'group', 'business', 'project', 'cabinet' ]


@login_required
def index(request):
    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    pass
    return render(request, 'assets/dashboard.html', locals())

def dashboard_test(request):
    pass
    return render(request, 'assets/dashboard_test.html', locals())


@login_required
def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())
