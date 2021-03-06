from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from cart.cart import Cart
from .forms import OrderForm
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required


def order_create_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, 
                                         product=item['product'], 
                                         price=item['price'], 
                                         quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderForm()
    return render(request, 'orders/order/create.html', {'form': form, 'title': 'Checkout'})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/detail.html', {'order': order})
    