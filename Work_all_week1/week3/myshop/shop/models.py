from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=200, null=False)
    enail = models.CharField(max_length=150, null=False)
    address = models.JSONField(null=True)   
    
class Cart(models.Model):
    customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, null=False)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    expired_in = models.IntegerField(null=False, default=60)
    
class CartItem(models.Model):
    cart = models.ForeignKey("shop.Cart", on_delete=models.CASCADE, null=False)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, null=False)
    amount = models.IntegerField(null=False, default=1)
    
class Order(models.Model):
    customer_id = models.ForeignKey("shop.Customer", on_delete=models.CASCADE, null=False)
    order_date = models.DateField(auto_now=False, auto_now_add=False)
    remark = models.TextField()
    
class OrderItem(models.Model):
    order =  models.ForeignKey("shop.Order", on_delete=models.CASCADE, null=False)
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE, null=False)
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=150, null=False)
    
class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    description = models.TextField()
    remaining_amount = models.IntegerField(default=0, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    Product_catagory = models.ManyToManyField(to='ProductCategory')
    
class Payment(models.Model):
    order = models.OneToOneField("shop.Order", on_delete=models.CASCADE, null=False)
    payment_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    remark = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    
class PaymentItem(models.Model):
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE, null=False)
    orderitem = models.OneToOneField("shop.OrderItem", on_delete=models.CASCADE, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)
    
class PaymentMethod(models.Model):
    payment = models.ForeignKey("shop.Payment", on_delete=models.CASCADE, null=False)
    QR = "01"
    CREDIT = "02"
    medthod_choice = {
        QR: "QR Payment",
        CREDIT: "Credit card Payment"
    }
    payment_method = models.CharField(
        max_length=6,
        choices=medthod_choice
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
        