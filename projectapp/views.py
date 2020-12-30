from django.shortcuts import render, redirect,HttpResponse
from .models import Products,Category,ProfilePic
from .forms import ProductModelForm, CategoryModelForm,RegistrationForm,EditUserForm,ProfilePicForm

from django.contrib.auth.forms import UserChangeForm,UserCreationForm,PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.decorators import permission_required,login_required

# Create your views here.

@login_required(login_url='/login')
def home(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    context={
        'products': products,
        'categories': categories
    }
    return render(request, 'home.html', context)

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

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
        else:
            return render(request,'add_product.html',{'form':form})
    else:
        form = ProductModelForm()
        return render(request,'add_product.html',{'form':form})

@login_required
def edit_product(request,id):
    product = Products.objects.get(id=id)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES,instance = product)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,'add_product.html',{'form':form})
    else:
        form = ProductModelForm(instance = product)
        return render(request,'add_product.html',{'form':form})

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