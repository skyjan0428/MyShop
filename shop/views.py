from django.shortcuts import render, redirect
from .models import Category, Product, OrderItem, Order
from decimal import Decimal
from django.conf import settings
from .forms import CartAddProductForm, OrderCreateForm
from django.views.decorators.http import require_POST
import random
# Create your views here.

def product_list(request, category_id=None):
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_id:
		category = Category.objects.get(id=category_id)
		products = products.filter(category=category)
	return render(request, 'list.html', locals())



def product_detail(request, product_id):
	product = Product.objects.get(id=product_id, available=True)
	cart_product_form = CartAddProductForm()
	return render(request, 'detail.html', locals())


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = Product.objects.get(id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product ,quantity=cd['quantity'], update_quantity=cd['update'])
	response = redirect('/cart_detail/')
	response.set_cookie("sid",cart.sid)
	return response

def cart_remove(request, product_id):
	cart = Cart(request)
	product = Product.objects.get(id=product_id)
	cart.remove(product)
	return redirect('/cart_detail/')

def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'], 'update':True})
	return render(request,'cart_detail.html', {'cart':cart})


def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
			cart.clear()
			return render(request, 'created.html', {'order':order})
	else:
		form = OrderCreateForm()
	return render(request, 'create.html', {'cart': cart, 'form':form})




class Cart(object):
	def __init__(self, request):
		sid = request.COOKIES['sessionid']
		if not sid:
			sid = random.randint(0,1000)

		self.session = request.session
		cart = self.session.get(sid)

		if not cart:
			cart = self.session[sid] = {}
		self.cart = cart
		self.sid = sid

	def add(self, product, quantity=1, update_quantity=False):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity':0, 'price':str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		self.session[self.sid] = self.cart
		self.session.modified = True

	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()


	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product
		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[self.sid]
		self.session.modified = True


