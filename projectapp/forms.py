from django import forms
from .models import Products,Category,ProfilePic
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name','price','image','description','category']
        labels = {'name':"Product's Name"}
        widget = {'price':'forms.TextInput'} 

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['pic']

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name']

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']