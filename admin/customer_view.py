from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.admin.views.decorators import staff_member_required
from store.models import Customer
from django.views import View


@staff_member_required(login_url='admin:login')
def customers(request):
    customers = Customer.objects.all()
    context = {'customers':customers}
    return render(request, 'admin/customer/index.html', context)