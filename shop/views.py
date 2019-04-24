from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    title = 'products'
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        print('category_slug', category_slug)
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)
        title = category.name
    
    return render(request, 'shop/product/list.html', {'category': category, 
                                                      'categories': categories, 
                                                      'products': products,
                                                      'title': title,
                                                     })

def product_detail(request, id, slug):
    cart_product_form = CartAddProductForm()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    return render(request, 'shop/product/detail.html', {'product': product, 
                                                        'title': product.name,
                                                        'cart_product_form': cart_product_form})

    
