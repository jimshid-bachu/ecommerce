from django.urls import path
from projectapp import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.add_product, name='add_product'),
    path('category/', views.add_category, name='add_category'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('category/<int:id>/', views.show_product, name = 'show_product'),
    path('register/', views.register, name = 'registerr'),
    path('login/', views.login_page, name = 'login_page'),
    path('logout/', views.logout_fn, name = 'logout_fn'),
    path('edit/user/', views.edit_user, name = 'edit_user'),
    path('password/', views.change_password, name = 'change_password'),

]