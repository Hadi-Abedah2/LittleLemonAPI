from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProxy(User):
    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    def __str__(self) -> str:
        return self.title
    class Meta:
        verbose_name_plural = 'Categories'

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    featured = models.BooleanField(db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self) -> str:
        return (f" {self.user.username} cart")
    def save(self, *args, **kwargs):
        self.unit_price = self.menu_item.price
        self.price = self.unit_price * self.quantity
        super(Cart, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('menu_item' ,'user')
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name= 'delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=00.00)
    date = models.DateField(db_index=True, auto_now_add=True)
    def calculate_total(self):
        total = sum(item.price for item in self.orderitem_set.all())
        return total
    def __str__(self) -> str:
        return (f" {self.user.username} order")
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self) -> str:
        return self.menu_item.title
    
    def save(self, *args, **kwargs):
        self.unit_price = self.menu_item.price
        self.price = self.unit_price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
        
        # After saving the OrderItem, update the related Order's total
        self.order.total = self.order.calculate_total()
        self.order.save()

    def delete(self, *args, **kwargs):
        super(OrderItem, self).delete(*args, **kwargs)
        
        # After deleting the OrderItem, update the related Order's total
        self.order.total = self.order.calculate_total()
        self.order.save()

    class Meta:
        unique_together = ('order', 'menu_item')
    
    
    

    

