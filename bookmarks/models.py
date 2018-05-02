from django.db import models
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
import datetime

#################################### MANAGER USING USERMODEL #####################################################################
####### FOR LOGIN###################
class LoginManager(models.Manager):
    def login(self,uname,pw):
        try:
            user = self.get(username=uname)
            if user.password == pw:
                return True
        except:
            return False

    def logincust(self,uname):
        try:
            user = self.get(username=uname)
            if user.role == 'N':
                return True
        except:
            return False
    def loginman(self,uname):
        try:
            user = self.get(username = uname)
            if user.role == 'F':
                return True
        except:
            return False
    def loginadmin(self,uname):
        try:
            user = self.get(username=uname)
            if user.username=='admin':
                return True
        except:
            return False
    def loginban(self,uname):
        try:
            user = self.get(username=uname)
            if user.banned==True:
                return True
        except:
            return False
    def loginapprove(self,uname):
        try:
            user = self.get(username=uname)
            if user.verified == True:
                return True
        except:
            return False
#----------------------------------------------
    def showall(self):
        p = UserModel.objects.all()
        return p
    def approve(self):
        p = UserModel.objects.all().filter(verified=False)
        return p



#########################################
class CategoryManager(models.Manager):
    def search(self,cat_name):
        item = self.get(category_name=cat_name)
        try:
            if item!=None:
                k=CategoryManager.all().filter(item.category_name == cat_name)
                print(k)
                return True
        except:
            return False
    def showall(self):
        k = Category.objects.all()
        return k

#########################################
class ProductManager(models.Manager):
    def unapprovedproduct(self):
        p = Products.objects.all().filter(valid = False)
        return p
    def check_bid_quantity(self,quant,prod):
        try:
            product = self.get(product_name=prod)
            q = product.quantity
            if q >= quant:
                return True
        except:
                return False

    def check_minbid(self,amount,prod):
        try:
            product = self.get(product_name = prod)
            amnt = product.minimum_bid
            if amnt <= amount:
                return True
        except:
            return False
    def searchall(self,key):
       # list_product_name = [Q(product_name__icontains=x) for x in key]
       # list_description = [Q(description__icontains=x) for x in key]
        r= self.filter(Q(product_name__icontains = key)|Q(description__icontains = key))
        return r
    def searchcat(self,key,cat):
        result = Products.objects.all().filter(category = cat)
        result_2 =result.filter(Q(product_name__icontains = key)|Q(description__icontains = key))
        return result_2

    def findownprodect(self,user):
        result = Products.objects.all().filter(seller = user)
        return result




########################################################################################################################
############################################# MODELS ###################################################################
########################################################################################################################

CHOICES =(
    ('N','Normal User'),
    ('F','Category Manager'),
)
class UserModel(models.Model):
    username = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nit_id = models.IntegerField(max_length=6)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    role = models.CharField(max_length=100,choices=CHOICES)
    verified = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)

    objects=LoginManager()
    def __unicode__(self):
        return '%s %s' %(self.first_name,self.last_name)

class Category(models.Model):
    category_name = models.CharField(max_length=30,unique=True)
    manager_name = models.ForeignKey(UserModel,blank=True,null=True)
    description = models.CharField(max_length=200)

    objects = CategoryManager()

    def __unicode__(self):
        return self.category_name


class UnApprovedProductManager(models.Manager):
    def get_query_set(self):
        return models.Manager.get_query_set(self).filter(valid = False)

class Products(models.Model):
    product_name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    image = models.ImageField(upload_to="product/img/")
    seller = models.ForeignKey(UserModel,blank=True,null=True)
    quantity = models.IntegerField()
    minimum_bid = models.IntegerField()
    bid_period = models.DateTimeField()
    valid = models.BooleanField(default=False)
    def __unicode__(self):
        return self.product_name

    objects = ProductManager()


class BidDetails(models.Model):
    name = models.ForeignKey(UserModel,blank=True,null=True)
    Product = models.ForeignKey(Products)
    bid_amount = models.IntegerField()
    bid_quantity = models.IntegerField()
    bid_time = models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return str(self.bid_amount)




class Comments(models.Model):
    name = models.ForeignKey(UserModel,blank=True,null=True)
    product = models.ForeignKey(Products)
    comment = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.datetime.now())
    def __unicode__(self):
        return str(self.name)
class CatMan(models.Model):
    Manager_name = models.CharField(max_length=30)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return self.Manager_name
