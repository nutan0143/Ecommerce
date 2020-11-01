import os
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import login,logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView
)

from .models import *
from.forms import *

class LoginView(View):
	"""Login User View"""
	def get(self,request):
		return render(request, 'login.html',{'type': 'login'})

	def post(self,request):
		params = request.POST
		try:
			user = User.objects.get(email_address=params['email_address'])
			if user:
				if user.is_active and user.check_password(params['password']):
					login(request,user,backend='django.contrib.auth.backends.ModelBackend')
					browser_cart = BrowserCart.objects.filter(browser_finger=params['fingerprint']).all()
					if browser_cart:
						for data in browser_cart:
							obj,create = Cart.objects.get_or_create(user=user,product=data.product,
								browser_finger=data.browser_finger)
							obj.total_product +=data.total_product
							obj.save()
							data.delete()
					return render(request, 'home.html', {
						'message': 'Login Successfull!'
					})
				error_message = 'Invalid Credentials.'
				return render(request, 'login.html',{'type': 'login', 'error_message': error_message})
			error_message = 'User Does Not Found.'
			return render(request, 'login.html',{'type': 'login', 'error_message': error_message})
		except Exception as e:
			error_message = "Account not registered."
			return render(request, 'login.html',{'type': 'login', 'error_message': error_message})


class SignupView(View):
	"""User Registration view"""
	def get(self,request):
		return render(request, 'login.html',
                      {'type': 'signup'})
	def post(self,request):
		params = request.POST
		try:
			user_obj = User.objects.filter(email_address=params['email_address']).first()
			if user_obj:
				context = {"message":"User Already exist with this email. Please login!","status":False}
				return JsonResponse(context)
			user_obj = User.objects.create(email_address=params['email_address'],name=params['name'])
			user_obj.is_active = True
			user_obj.set_password(params['password'])
			user_obj.save()
			context = {"message":"Signup Successfully","status":True}
			return JsonResponse(context)
		except Exception as e:
		    context = {"message": "Something Went wrong!. Please login!", "status": False}
		    return JsonResponse(context)


class HomeView(View):
	"""Home View"""
	def get(self,request):
		women = Product.objects.filter(type_of_product='women')[:6]
		men = Product.objects.filter(type_of_product='men')[:4]
		kid = Product.objects.filter(type_of_product='Kids')[:4]
		return render(request,'home.html',{"women":women,"men":men,"kid":kid})


class BlogView(TemplateView):
	"""Blog View"""
	template_name = "blog.html"


class ProductView(View):
	"""Product listing view"""
	def get(self,request):
		try:
			type = request.GET.get('type')
			search = request.GET.get('search')
			min_price = request.GET.get('min_price')
			max_price = request.GET.get('max_price')
			product_obj = Product.objects.all()
			if type == 'men':
				product_obj = product_obj.filter(type_of_product='men')
			elif type == 'women':
				product_obj = product_obj.filter(type_of_product='women')
			elif type == 'kid':
				product_obj = product_obj.filter(type_of_product='Kids')
			elif type == 'house':
				product_obj = product_obj.filter(type_of_product='household')

			if search:
				product_obj = product_obj.filter(Q(product_name__icontains=search) | Q(decription__icontains=search))

			if min_price and max_price:
				product_obj = product_obj.filter(Q(price__gte=min_price) & Q(price__lte=max_price))
			if product_obj:
				return render(request,'product.html',{"product_data":product_obj[:12],"status":True,"type":type})
			return render(request,'product.html',{"product_data":"","status":False,"type":type})
		except Exception as e:
			return render(request,'product.html',{"product_data":"","status":False,"type":type})

	def post(self,request):
		try:
			params = request.POST
			fingerprint = request.GET.get('fingerprint')
			if request.user.is_authenticated:
				obj, create = Cart.objects.get_or_create(user_id=request.user.id,product_id=params['product_id'])
				obj.total_product = obj.total_product+1
				obj.browser_finger=fingerprint
				obj.save()
				return JsonResponse({"message":"Item has added to cart Successfully"})
			else:
				obj, create = BrowserCart.objects.get_or_create(browser_finger=fingerprint,product_id=params['product_id'])
				obj.total_product = obj.total_product+1
				obj.save()
				return JsonResponse({"message":"Item has added to cart Successfully"})
		except Exception as e:
			return JsonResponse({"message":"Something Went Wrong."})


class CartView(View):
	"""Cart view"""
	def get(self,request):
		fingerprint = request.GET.get('fingerprint')
		cart_data = []
		if request.user.is_authenticated:
			cart = Cart.objects.filter(user_id=request.user.id)
		else:
			cart = BrowserCart.objects.filter(browser_finger=fingerprint)
		if not cart:
			return render(request, 'cart.html'.format(fingerprint), {"data":"","status":False})
		for data in cart:
			cart_data.append({
				"product_name":data.product.product_name,
				"image":data.product.image,
				"price":data.product.price,
				"cart_id":data.id,
				"total_product":data.total_product,
				"total_price":data.total_product*data.product.price	
			})
		return render(request, 'cart.html', {"data":cart_data,"status":True})

	def put(self,request):
		try:
			fingerprint = request.GET.get('fingerprint')
			id = request.GET.get('id')
			type = request.GET.get('type')
			if request.user.is_authenticated:
				cart = Cart.objects.filter(id=id).first()
			else:
				cart = BrowserCart.objects.filter(id=id).first()
			if type == 'add':
				cart.total_product +=1
				cart.save()
				return JsonResponse({"status":True})
			else:
				if cart.total_product == 1:
					cart.delete()
				else:
					cart.total_product -=1
					cart.save()
				return JsonResponse({"status":True})
		except Exception as e:
			return JsonResponse({"status":False})
		
	def delete(self,request):
		try:
			fingerprint = request.GET.get('fingerprint')
			id = request.GET.get('id')
			if request.user.is_authenticated:
				cart = Cart.objects.filter(id=id).delete()
			else:
				cart = BrowserCart.objects.filter(id=id).delete()
			return JsonResponse({"status":True})
		except Exception as e:
			return JsonResponse({"status":False})

class UserLogout(LoginRequiredMixin, TemplateView):
	"""User logout action"""
	def get(self, request):
		logout(request)
		return redirect('app:homeview')

