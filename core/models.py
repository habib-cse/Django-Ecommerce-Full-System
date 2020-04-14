from django.db import models
from django.utils.html import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=12)
    status = models.BooleanField(default=True)
    joining_date = models.DateField(auto_now_add=True) 

    class Meta:  
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.name
 
class Category(models.Model):
    cat_name = models.CharField(max_length=150)
    cat_status  = models.BooleanField(default=True) 

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categorys"

    def __str__(self):
        return self.cat_name 

class SubCategory(models.Model):
    subcat_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcat_status = models.BooleanField(default=True) 

    class Meta: 
        verbose_name = 'Product Sub Category'
        verbose_name_plural = 'Product Sub Categorys' 

    def __str__(self):
        return self.subcat_name

class GalaryImage(models.Model):
     images = models.ImageField(upload_to='upload')
     time_stamp = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.images.url
     

     class Meta: 
        verbose_name = 'Galary Image'
        verbose_name_plural = 'Galary Images'


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=20)
    coupon_amount = models.FloatField()
    coupon_status = models.BooleanField(default=True)
    coupon_start_date = models.DateTimeField()
    coupon_end_date = models.DateTimeField()

    class Meta: 
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'

    def __str__(self): 
        return self.coupon_code
  
class Product(models.Model):

    PRODUCT_STATUS = (
        ('IS',"In Stock"),
        ('SO',"Stock Out"),
        ('AO',"Accepting Order") 
    ) 
    name = models.CharField(max_length=100)
    title = models.CharField(blank=True, max_length=150)
    new_arival = models.BooleanField(default = False)
    regular_price = models.FloatField(default=0)
    discount_price = models.FloatField(blank=True,null=True)
    offer_price   =  models.FloatField(blank=True, null=True)
    top_optional_text = models.TextField(blank=True)
    Bottom_optional_text = models.TextField(blank=True) 
    product_status = models.CharField(max_length=2, choices= PRODUCT_STATUS, default="IS")
    product_galary_image = models.ManyToManyField(GalaryImage)
    product_thumbnail = models.ImageField(upload_to='upload') 
    product_cateogry = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    time_stamp = models.DateTimeField(auto_now_add=True) 
    cash_on_delivery = models.BooleanField(default=False)
    slug = models.SlugField(unique=False,null=True, blank=True) 

    if discount_price:
        def takaoff(self):
            return self.regular_price - self.discount_price

    def main_price(self):
        if self.offer_price and self.discount_price:
            main_price = self.discount_price - (self.discount_price * self.offer_price)/100  
        elif self.offer_price and self.regular_price:
            main_price = self.regular_price - (self.regular_price * self.offer_price)/100
        elif self.discount_price:
            main_price = self.discount_price
        else:
            main_price = self.regular_price
        return main_price
             
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products" 

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class ProductReview(models.Model):
    review_number = models.DecimalField(default=5.0, max_digits=3, decimal_places=1)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review_date = models.DateField(auto_now_add=True) 
    review_content = RichTextField()
 
    class Meta: 
        verbose_name = 'ProductReview'
        verbose_name_plural = 'ProductReviews'

    def __str__(self):
       return("{}, {} = {}".format(self.review_user, self.product, self.review_number))
 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 

    class Meta:  
        verbose_name = 'Card Item'
        verbose_name_plural = 'Card Items'

    def __str__(self): 
        return("{} => {} ==> {}".format(self.user.name, self.product.name, self.quantity))

    def card_price(self):
        card_prices = self.product.main_price() * self.quantity
        return card_prices


class AddtoCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderItem) 
    price = models.FloatField(default=0)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    
    
    class Meta: 
        verbose_name = 'Add to Card'
        verbose_name_plural = 'Add to Cards'

    def __str__(self): 
        return ("{} {} {}".format(self.user, self.products.name,self.quantity ))

