from django.shortcuts import render
from django.db.models import Q
# Create your views here.
from django import template
from django.shortcuts import redirect, render
from django.http.response import HttpResponseRedirect
from django.http import HttpResponse, request
from django.template import loader
from . import models
import operator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    if request.session.session_key == None:
        request.session.create() 
        request.session['cart']='created'

    cartLength = ''
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count()
    except:
        pass    
    category = models.category.objects.all()
    session_key = request.session.session_key
    return HttpResponse(template.render({'category':category,'cart_length':cartLength,'session':session_key},request))


def product_details_view(request,category):

    template = loader.get_template('display.html')
    categoryId = models.category.objects.get(category = category)
    cartLength = models.cart.objects.filter(session_key= request.session.session_key).count()
    cId = categoryId.id
    brand = models.brand.objects.all()
    products = models.product.objects.filter(category_id = categoryId.id)
    return HttpResponse(template.render({'brand':brand,'product':products,'cart_length':cartLength,'category':cId,'category_name':category,'sessionKey':request.session.session_key},request))


def cart(request):

    template = loader.get_template('cart.html')

    cartLength = ''
    subTotal = ''
    cartData = []
    cartLength =''
    try:
        data = models.cart.objects.filter(session_key = request.session.session_key)
        print(len(data))
        for i in data:
            print(i.product.product_image.url)
            data1 = {
                'id':i.id,
                'name':i.product.product_name,
                'model':i.product.model,
                'image':i.product.product_image.url,
                'quantity':i.quantity,
                'price':i.product.price,
                'sub_total':int(i.quantity) * int(i.product.price)               
            }
            print(data1)
            cartData.append(data1)
        subTotal = sum(map(operator.itemgetter('sub_total'),cartData))
        print(subTotal)
    except Exception as e:
        pass
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count() 
    except Exception as e:
        pass

    
    return HttpResponse(template.render({'cart_length':cartLength,'cart_data':cartData,'data':data,'total':subTotal,'sessionKey':request.session.session_key},request))



def checkout(request):

    template = loader.get_template('checkout.html')
    subTotal = ''
    data = []
    messagestring = ''
    cartLength =''
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count() 

        if request.method == "POST":
            name = request.POST.get('name')
            address = request.POST.get('address')
            phone = request.POST.get('number')
        subTotal = sum(map(operator.itemgetter('sub_total'),data))  
        return redirect('/order_send_to_whatsaapp/'+name+'/'+address+'/'+phone) 
    except Exception as e:
        pass

    return HttpResponse(template.render({'cart_length':cartLength},request))


def send_to_whatsapp(request,name,address,phone):

    template = loader.get_template('sendwhatsapp.html')
    name = name
    address = address
    phone = phone
    messagestring = ''
    grandtotal=0
    data = []
    cartLength = ''
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count() 
        messagestring = 'https://wa.me/9660590099210?text=Name :'+name+'%0aAddress :'+address+'%0aPhone :'+phone+\
            "%0a-----Order Details------"
        cartData = models.cart.objects.filter(session_key = request.session.session_key)
        for i in cartData:
            data1 = {
                'id':i.product.product_name,
                'name':i.product.model,
                'quantity':i.quantity,
                'price':i.product.price,
                'sub_total':int(i.quantity) * int(i.product.price)               
            }
            data.append(data1)
            grandtotal+=int(i.quantity) * int(i.product.price)   
        for i in data:
            messagestring +="%0aProduct-Id:"+str(i['id'])+"%0aName:"+str(i['name'])+"%0aQty:"+str(i['quantity'])+"%0aPrice:"+str(i['price'])+"%0aTotal :"+str(i['sub_total'])+"%0a-----------------------------"
        messagestring+="%0a-----------------------------%0a\
        Grand Total :"+str(grandtotal)+"%0a--------------------------------"
        # del request.session['cartdata']

    except:

        pass        

    return HttpResponse(template.render({'cart_length':cartLength,'link':messagestring,'name':name,'address':address,'phone':phone},request))



def about(request):

    template = loader.get_template('about.html')
    cartLength = ''
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count() 
    except:
        pass
    return HttpResponse(template.render({'cart_length':cartLength},request))


def contact(request):

    template = loader.get_template('contact.html')
    cartLength =''
    try:
        cartLength = models.cart.objects.filter(session_key= request.session.session_key).count() 
    except:
        pass
    return HttpResponse(template.render({'cart_length':cartLength},request))



@method_decorator(csrf_exempt)
def search_items(request):
    if request.POST:
        search_Key=request.POST['search_Key']
        prductlist = models.product.objects.filter(Q(product_name__icontains=search_Key) | Q(model__model_name__icontains=search_Key)| Q(category__category__icontains=search_Key)| Q(brand__brand_name__icontains=search_Key))

        # if request.GET['category']:
            
        #     cID=request.GET['category']
        #     if cID!='0':
        #         print('category Not Zer '*20)
        #         prductlist=prductlist.filter(category__id=cID)
        # if request.GET['brand']:
        #     bID=request.GET['brand']
        #     if bID!='0':
        #         prductlist=prductlist.filter(brand__id=bID)
        # if request.GET['model']:
        #     mID=request.GET['model']
        #     if mID!='0':
        #         prductlist=prductlist.filter(model__id=mID)
        jsonProductList=[]
        for product in prductlist:
            data={
                "id":product.id,
                "product_name":product.product_name,
                "category":product.category.category,
                "brand":product.brand.brand_name,
                "model":product.model.model_name,
                "product_image":product.product_image.url,
                "price":product.price,
            }
            jsonProductList.append(data)

        return JsonResponse({"jsonProductList":jsonProductList})
    return JsonResponse({"Message":"Only POST method Allowed "})
