import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
class BaseModel(models.Model):
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		abstract=True


class MyUserManager(BaseUserManager):

    def create_superuser(self, username, password):
        user = self.model(email_address=email_address)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_user(self, email_address, password=None, username=''):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email_address:
            raise ValueError('Users must have an Email Address')

        user = self.model(
            email_address=self.email_address,
            is_active=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    """
        User information
    """
    email_address = models.EmailField(
        "Email Address", unique=True, max_length=50, null=True, blank=True
    )
    name = models.CharField(
        "First Name", max_length=100, blank=True, null=True
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False
    )
    is_superuser = models.BooleanField(
        "Super User", default=False
    )
    is_staff = models.BooleanField(
        "Staff", default=False
    )
    is_active = models.BooleanField(
        "Status", default=True
    )
    is_online = models.BooleanField(
        "User is online", default=False
    )

    objects = MyUserManager()
    USERNAME_FIELD = 'email_address'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email_address

class Product(BaseModel):
    """Product Information"""
    product_name = models.CharField("Product Name", max_length=100)
    image = models.TextField("Image")
    type_of_product = models.CharField("Type of product",max_length=100)
    decription = models.TextField("Description")
    price = models.IntegerField("Product price")

    def __Str__(self):
        return self.product_name

class Cart(BaseModel):
	"""User Cart Information"""
	browser_finger = models.CharField("Browser finger print",max_length=225, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	total_product = models.IntegerField("Total product", default=0)

	def __str__(self):
		return self.user.email_address

class BrowserCart(BaseModel):
	"""Browser cart Information"""
	browser_finger = models.CharField("Browser finger print",max_length=225)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	total_product = models.IntegerField("Total product", default=0)
	def __str__(self):
		return self.user.browser_finger
