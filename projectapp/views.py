from django.shortcuts import render, redirect,HttpResponse
from .models import Products,Category,ProfilePic,Cart
from .forms import ProductModelForm, CategoryModelForm,RegistrationForm,EditUserForm,ProfilePicForm

from django.contrib.auth.forms import UserChangeForm,UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

import json
from django.http import JsonResponse

class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'home.html'
    model = Products
    # queryset = Products.objects.filter(price__gt = 102000)
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context



class ProductDetailView(LoginRequiredMixin, DetailView):
    template_name = 'product_detail.html'
    model = Products
    context_object_name = 'product'


class CreateProductView(LoginRequiredMixin, CreateView):
    template_name = 'add_product.html'
    model = Products
    fields = ['name','price','image','description','category']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('home')


class EditProductView(LoginRequiredMixin, UpdateView):
    template_name = 'add_product.html'
    model = Products
    fields = ['name','price','image','description','category']
    success_url = '/'


class DeleteProductView(LoginRequiredMixin, DeleteView):
    template_name = 'add_product.html'
    model = Products
    success_url = '/'









# @login_required(login_url='/login')
# def home(request):
#     products = Products.objects.all()
#     categories = Category.objects.all()
#     context={
#         'products': products,
#         'categories': categories
#     }
#     return render(request, 'home.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,'add_category.html',{'form':form})
    else:
        form = CategoryModelForm()
        return render(request,'add_category.html',{'form':form})

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.user = request.user
#             obj.save()
#             return redirect('home')
#             messages.add_message(request,'Hello world.')
#         else:
#             return render(request,'add_product.html',{'form':form})
#     else:
#         form = ProductModelForm()
#         return render(request,'add_product.html',{'form':form})

# @login_required
# def edit_product(request,id):
#     product = Products.objects.get(id=id)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES,instance = product)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             return render(request,'add_product.html',{'form':form})
#     else:
#         form = ProductModelForm(instance = product)
#         return render(request,'add_product.html',{'form':form})

@login_required
def delete_product(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('home')

@login_required
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('home')

@login_required
def show_product(request,id):
    category = Category.objects.get(id=id)
    products = category.products_set.all()
    categories = Category.objects.all()
    context = {
        'products':products,
        'categories':categories
    }
    return render(request,'show_product.html',context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form1 = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save() 
            if form1.is_valid():
                obj2 = form1.save(commit=False)
                obj2.user = obj
                obj2.save()
            return redirect('home')
        else:
            return render(request,'register.html',{'form':form,'form1':form1})
    else:
        form = RegistrationForm()
        form1 = ProfilePicForm()
        return render(request,'register.html',{'form':form, 'form1':form1})

@login_required(login_url='/login/')
def edit_user(request):
    profilepic = ProfilePic.objects.get(user = request.user)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance = request.user)
        form1 = ProfilePicForm(request.POST, request.FILES, instance = profilepic)
        if form.is_valid():
            obj = form.save() 
            if form1.is_valid():
                obj2 = form1.save(commit=False)
                obj2.user = obj
                obj2.save()
            return redirect('home')
        else:
            return render(request,'register.html',{'form':form, 'form1':form1})
    else:
        form = EditUserForm(instance = request.user)
        form1 = ProfilePicForm(instance=profilepic)
        return render(request,'register.html',{'form':form,'form1':form1})

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse('username or password incorrect')
    return render(request, 'login.html')

def logout_fn(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
        else:
            return render(request,'register.html',{'form':form})
    else:
        form = PasswordChangeForm(user = request.user)
        return render(request,'register.html',{'form':form})


def fetch_products(request):
    products = list(Products.objects.values())
    return JsonResponse(products, safe=False)


def addtocart(request,id):
    product = Products.objects.get(id=id)
    user = request.user
    addcart = Cart.objects.filter(product=product,user=user)
    if addcart:
        addcart[0].delete()
    else:
        Cart.objects.create(product=product,user=user)
    cart_count = Cart.objects.filter(user=user)
    # return HttpResponse(str(len(count)))
    return redirect('/')

def showcart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'cart.html',{'cart_items':cart_items})
    # return render(request, 'products/base.html',{'length':item_num})

def removecart(request, id):
    cart_item = Cart.objects.get(id=id)
    cart_item.delete()
    return redirect('showcart')

