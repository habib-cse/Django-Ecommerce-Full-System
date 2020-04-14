from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import View, DetailView
from django.contrib import messages  
from .forms import ProductReviewForm
from .models import (Category,
 Coupon,
 GalaryImage,
 Product,
 User,
 ProductReview,
 AddtoCard,
 OrderItem)

# Create your views here.
 
class HomepageView(View):
    def get(self, *args, **kwargs):
        products = Product.objects.all() 
        context = {
            'products':products
        } 
        return render(self.request, 'frontend/index.html',context)


def product_details(request,slug): 

    product = get_object_or_404(Product, slug=slug)
    review = ProductReview.objects.filter(product_id=product.id) 
    total_user = review.count()
    if total_user > 0:
        total_review = 0
        for reviews in review:
            total_review += reviews.review_number 
        avg_review = total_review/total_user
    else:
        avg_review = 0
    if request.method == "GET":
        form = ProductReviewForm()  
        
    if request.method =="POST":
        user_id = request.session['id'] 
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review_number = form.cleaned_data['review_number']
            review_content = form.cleaned_data['review_content']
            add_review = ProductReview(review_number=review_number, review_user_id=user_id,product_id=product.id,review_content=review_content)
            add_review.save() 

    context = { 
        'form':form,
        'review':review,
        'product':product,
        'avg_review':avg_review,
        'total_user':total_user
    }  
    return render(request,'frontend/product_details.html',context)
  

def UserRegistration(request):
    if request.method == "POST":
        username = request.POST['name']
        useremail = request.POST['email']
        userpass = request.POST['password']
        user_check = User.objects.filter(email=useremail)
        if user_check.exists():
            messages.error(request,"User already Exsits")
        else:
            User.objects.create(name=username, email=useremail, password=userpass)
            messages.success(request,"Congratulations {}, You are Successfully Signup".format(username))
    
    return render(request, 'frontend/user_registration.html')


def UserLogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user_prevelize = User.objects.filter(email=email, password=password, status=True).first()
        if user_prevelize:
            request.session['user'] = user_prevelize.name
            request.session['id'] = user_prevelize.id
            messages.success(request, "Hi {} You have login Successfully".format(user_prevelize.name))
            return redirect('core:home')
        else:
            messages.error(request, "Emaill or password is not correct")
    return render(request, 'frontend/user_registration.html')


def UserLogout(request):
    del request.session['user']
    del request.session['id']
    return redirect('core:login')

def AddToCard(request,id):  
    try:
        if request.session['id']:  
            userid = request.session['id'] 
            item = get_object_or_404(Product, id=id)
            order_item, created = OrderItem.objects.get_or_create(user_id = userid, product_id = id)
            order_check = AddtoCard.objects.filter(user_id=userid)
            if order_check.exists():
                order = order_check[0]
                if order.products.filter(product_id = id).exists():
                    order_item.quantity += 1
                    order_item.save() 
                    messages.success(request, '{} in exists, Quantity Increased'.format(item))
                else:
                    messages.success(request, '{} added to card'.format(item))
                    order.products.add(order_item)
            else:
                new_user_order = AddtoCard.objects.create(user_id=userid)
                new_user_order.products.add(order_item) 
                messages.success(request, '{} added to card'.format.format(item))
            url = request.path 
            return redirect('core:home')
        else:
            return redirect('core:login') 
    except:
        return redirect('core:login')

def checkout(request,id):
    order_items = OrderItem.objects.filter(user_id = id)
    total_numberof_items = order_items.count() 
    complete_price = 0.0
    for item in order_items:
        complete_price =complete_price + item.card_price()

    context = {
        'order_items':order_items,
        'total_number':total_numberof_items,
        'complete_price':complete_price
    }

    return render(request, 'frontend/checkout.html',context)

def remove_from_card(request, id):
    OrderItem.objects.filter(product_id=id).delete()
    messages.success(request,"Item removed from card")
    return redirect('core:checkout', id=request.session['id'])

def card_update(request):
    if request.method == "POST":
        obj = OrderItem.objects.filter(user_id = request.session['id'])
        i=0
        for item in obj:
            i+=1
            quantity = request.POST['amount_'+str(i)] 
            item.quantity = quantity
            item.save()
            print(quantity)
            quantity = " "

    return redirect('core:checkout', id=request.session['id'])

def check_product(product):
    return product != "" and product is not None
       

def product_search(request): 
    query = Product.objects.all() 
    lower_pirce = 10
    upper_pirce = 500000

    if request.method=="POST":  
        product_name = request.POST["product"]
        lower_pirce = request.POST.get("lower_pirce")
        upper_pirce = request.POST.get("upper_pirce") 


        if check_product(product_name):
            query = query.filter(name__icontains = product_name)
        
        if check_product(lower_pirce) and check_product(upper_pirce):
            query = query.filter(regular_price__gte=lower_pirce, regular_price__lte=upper_pirce)
        
    context = {
        'products':query,
        'lower_pirce':lower_pirce,
        'upper_pirce':upper_pirce
    }

    return render(request,'frontend/product_search.html',context)