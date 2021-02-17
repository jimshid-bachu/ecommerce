from django.urls import path
from projectapp import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/showcart/', views.showcart, name='showcart'),
     path('product/removecart/<int:id>/', views.removecart, name='removecart'),
    path('product/', views.CreateProductView.as_view(), name='add_product'),
    path('product/<pk>/', views.ProductDetailView.as_view()),
    path('category/', views.add_category, name='add_category'),
    path('product/edit/<pk>/', views.EditProductView.as_view(), name='edit_product'),
    path('delete/<pk>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('category/<int:id>/', views.show_product, name = 'show_product'),
    path('register/', views.register, name = 'registerr'),
    path('profilepic/', views.register, name = 'profilepic'),
    path('login/', views.login_page, name = 'login_page'),
    path('logout/', views.logout_fn, name = 'logout_fn'),
    path('edit/user/', views.edit_user, name = 'edit_user'),
    path('password/', views.change_password, name = 'change_password'),

    path('product/addtocart/<int:id>/', views.addtocart, name='addtocart'),
   

    path('api/products/', views.fetch_products)

]