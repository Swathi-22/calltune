from django.http.response import JsonResponse
from django.shortcuts import render
import json
from web.models import category, product
from web import models
import operator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt)
def select_model(request):
    a = []
    products = []   
    brand = request.POST['brand']
    category = request.POST['category']
    try:
        model = models.product_model.objects.filter(
            brand_id=brand, category_id=category)
        print(model)
        for i in model:
            data = {
                'id': i.id,
                'model': i.model_name
            }
            a.append(data)
        if brand == '0':
            selectImage = models.product.objects.filter(category_id=category)
            for j in selectImage:
                md = models.product_model.objects.get(id=j.model_id)
                br = models.brand.objects.get(id=j.brand_id)
                data1 = {
                    'id': j.id,
                    'name': j.product_name,
                    'image': j.product_image.url,
                    'brand': br.brand_name,
                    'model': md.model_name,
                    'price': j.price
                }
                products.append(data1)
            for i in products:
                print(i)
        else:
            selectImage = models.product.objects.filter(
                brand_id=brand, category_id=category)
            br = models.brand.objects.get(id=brand)
            for j in selectImage:
                md = models.product_model.objects.get(id=j.model_id)
                data1 = {
                    'id': j.id,
                    'name': j.product_name,
                    'image': j.product_image.url,
                    'brand': br.brand_name,
                    'model': md.model_name,
                    'price': j.price
                }
                products.append(data1)
            for i in products:
                print(i)
    except:
        pass
    return JsonResponse({'data': a, 'product': products})


@method_decorator(csrf_exempt)
def select_model_based_images(request):
    a = []
    brand = request.POST['brand']
    model = request.POST['model']
    category = request.POST['category']
    br = models.brand.objects.get(id=brand)
    md = models.product_model.objects.get(id=model)
    try:
      
        selectImage = models.product.objects.filter(
            brand_id=brand, category_id=category, model_id=model)
        for i in selectImage:
            data = {
                'id': i.id,
                'name': i.product_name,
                'image': i.product_image.url,
                'brand': br.brand_name,
                'model': md.model_name,
                'price': i.price
            }
            a.append(data)
        for i in a:
            print(a)
        
    except Exception as e:
        pass
    return JsonResponse({'data': a})


@method_decorator(csrf_exempt)
def cart(request):
    msg = ''
    
    cartLength = ''
    product_id = request.POST['product_id']
    sessionId = request.POST['session']
    checkCart = models.cart.objects.filter(session_key = sessionId,product_id = product_id)
    if checkCart.exists():
        msg = '1'
    else:


        saveCart = models.cart()
        saveCart.product_id = product_id
        saveCart.session_key = sessionId
        saveCart.quantity = 1
        saveCart.save()
        msg = '0'

    cartLength = models.cart.objects.filter(session_key= sessionId).count()

   
    return JsonResponse({'length': cartLength, 'msg': msg})


@method_decorator(csrf_exempt)
def cart_delete(request):
    cartLength = ''
    id = request.POST['product_id']
    sessionId = request.POST['session']
    price = ''
    try:
        deleteProduct = models.cart.objects.get(id = id)
        prce = deleteProduct.product.price
        qty = deleteProduct.quantity
        price = qty * prce
        deleteProduct.delete()
        cartLength = models.cart.objects.filter(session_key= sessionId).count()
    except Exception as e:
        pass
    return JsonResponse({'length': cartLength, 'price': price})


@method_decorator(csrf_exempt)
def update_cart(request):
    productId = request.POST['product_id']
    quantity = request.POST['quantity']
    sessionId = request.POST['session']
    qty = ''
    price = ''
    qty1 = ''
    cartData = []
    subTotal = ''
    try:
        updateCart = models.cart.objects.get(id = productId)
        updateCart.quantity = quantity
        updateCart.save()
        price = updateCart.product.price
        data = models.cart.objects.filter(session_key = sessionId)
        for i in data:
            print(i.product.product_image.url)
            data1 = {
                'id':i.id,
                'name':i.product,
                'image':i.product.product_image.url,
                'quantity':i.quantity,
                'price':i.product.price,
                'sub_total':int(i.quantity) * int(i.product.price)               
            }
            cartData.append(data1)
        subTotal = sum(map(operator.itemgetter('sub_total'),cartData))
    except Exception as e:
        pass
    return JsonResponse({'quantity': quantity, 'price': price, 'sub_total': subTotal})


@method_decorator(csrf_exempt)
def select_models(request):
    a = []
    brand = request.POST['brand']
    category = request.POST['category']
    model = models.product_model.objects.filter(
        category_id=category, brand_id=brand)
    for i in model:
        data = {
            'id': i.id,
            'model': i.model_name
        }
        a.append(data)
    return JsonResponse({'data': a})
