from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user, allowed_users
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from store.models import *
from django.views import View
from django.template.defaultfilters import slugify

@staff_member_required(login_url='admin:login')
def contacts(request):
    contacts = Contact.objects.all()
    context = {'contacts':contacts}
    return render(request, 'admin/contact/index.html' , context)


@method_decorator(staff_member_required, name='dispatch')
class ContactDelete(LoginRequiredMixin, View):
    login_url = 'admin:login'
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        try:
            contact = Contact.objects.get(id=id)
        except:
            messages.error(request,'Liên hệ không tồn tại')
            return redirect('admin:contacts')
        context = {'contact':contact}
        return render(request, 'admin/contact/delete.html', context)

    def post(self, request, id):
        try:
            contact = Contact.objects.get(id=id)
        except:
            messages.error(request,'Liên hệ không tồn tại')
            return redirect('admin:contacts')
        contact.delete()
        messages.success(request,'Xóa liên hệ từ "'+contact.full_name+'" thành công')
        return redirect('admin:contacts')