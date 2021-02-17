from projectapp.models import Products,Category,ProfilePic,Cart
from django.shortcuts import HttpResponse
def parallel(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        return {'cart_count':cart_count,'categories':categories}
    else:
        return {'categories':categories}

