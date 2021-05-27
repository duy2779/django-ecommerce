from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    gender_choice = ((0,'Nữ'),(1,'Nam'),(2,'Không xác định'))
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.username


    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url =''
        return url

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"

    def __str__(self):
        return self.name

    @property
    def get_order_done(self):
        orders = self.order_set.filter(status=2).count()
        return orders


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    slug = models.SlugField(max_length=255, blank=False, unique=True)
    parent_id = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="category_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="category_updated_by")
    status = models.IntegerField(default=0)


    class Meta:
        unique_together = ('slug', 'parent_id',)
        verbose_name = "Loại sản phẩm"
        verbose_name_plural = "Loại sản phẩm"

    def __str__(self):
        full_path = [self.name]
        k = self.parent_id
        while k is not None:
            full_path.append(k.name)
            k = k.parent_id
        return ' / '.join(full_path[::-1])


class Contact(models.Model):
    full_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    phone = models.CharField(max_length=11, blank=True)
    message = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Liên hệ"
        verbose_name_plural = "Liên hệ"

    def __str__(self):
        return self.full_name


class Topic(models.Model):
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, blank=False)
    parent_id = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="topic_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name="topic_updated_by")
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Chủ đề"
        verbose_name_plural = "Chủ đề"

    def __str__(self):
        return self.name

class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, blank=False)
    detail = models.TextField(blank=False)
    img = models.ImageField(null=True, blank=True)
    type = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="post_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name="post_updated_by")
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url =''
        return url

    def delete(self, *args, **kwargs):
        self.img.delete()
        super().delete(*args, **kwargs)

class Menu(models.Model):
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.SET_NULL)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255, blank=False)
    link = models.CharField(max_length=255, blank=False)
    type = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    parent_id = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="menu_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name="menu_updated_by")
    status = models.IntegerField(default=0)


    def __str__(self):
        full_path = [self.name]
        k = self.parent_id
        while k is not None:
            full_path.append(k.name)
            k = k.parent_id
        return ' / '.join(full_path[::-1])


class Product(models.Model):
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=False)
    featured_choice = ((True,'Bật'),(False,'Tắt'))
    featured = models.BooleanField(default=False, choices=featured_choice)
    img = models.ImageField(null=True, blank=True)
    price = models.DecimalField(blank=False, null=False, max_digits=10, decimal_places=0)
    price_sale = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name="product_updated_by")
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.img.delete()
        super().delete(*args, **kwargs)


    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url =''
        return url


class Order(models.Model):
    status_choice = ((0,'Giỏ hàng'),(1,'Chờ nhận'),(2,'Hoàn thành'))
    code = models.CharField(max_length=50)
    payment_method = models.IntegerField(default=0, null=False, blank=False)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=False, null=True)
    created_date = models.DateTimeField(default=timezone.datetime.now())
    export_date = models.DateTimeField(null=True)
    delivery_address = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,related_name="order_updated_by")
    status = models.IntegerField(default=0, choices=status_choice)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return self.delivery_address

    @property
    def get_cart_total(self):
        orderitems = self.order_detail_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_detail_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_amount(self):
        orderitems = self.order_detail_set.all()
        total = sum([item.quantity*item.product.price for item in orderitems])
        return total


class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=False, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=False, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class Banner(models.Model):
    link = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255, blank=True)
    detail = models.CharField(max_length=255, blank=True)
    img = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.datetime.now())
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="banner_created_by")
    updated_at = models.DateTimeField(default=timezone.datetime.now())
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="banner_updated_by")
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name


    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url =''
        return url