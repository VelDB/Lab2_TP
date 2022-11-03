from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .models import Product, Purchase

# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        purchase = form.save(commit=False)
        product = purchase.product
        if product.amount == 0:
            return HttpResponse("<h1>400 Bad Request</h1>"
                                "<br>Продукта нет в наличии!", status=400)
        product.amount -= 1
        product.save()
        purchase.save()
        return HttpResponse(f'Спасибо за покупку, {purchase.person}!')

