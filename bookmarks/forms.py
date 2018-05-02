from django import forms
from bookmarks import models
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['username','password']

class SignUp(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['role','first_name','last_name','nit_id','address','mobile','email','username','password',]
        widgets = {'address':forms.Textarea(),'password':forms.PasswordInput()}
    password1 = forms.CharField(max_length= 30, widget= forms.PasswordInput(),label=u'verify password')
class Login(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=10,widget=forms.PasswordInput())

class PlaceAdd(forms.ModelForm):
    class Meta:
        model = models.Products
        exclude = ['valid']
        widgets = {'description':forms.Textarea(),'seller':forms.HiddenInput()}
        upload_image = forms.ImageField()

class AddCat(forms.ModelForm):
    class Meta:
        model = models.Category
        #exclude = ['manager_name']
        widgets = {'description':forms.Textarea(),'manager_name':forms.HiddenInput()}

class Search(forms.Form):
    enter_keyword =forms.CharField(max_length=30,required=False)
    category = forms.ChoiceField(choices=([('0','all')].__add__(list(models.Category.objects.values_list('id','category_name')))))
    #def __init__(self,*args,**kwargs):
     #   super(Search,self).__init__(*args,**kwargs)
      #  self.fields['category']=forms.ChoiceField(choices=[(o.category_name,str(o)) for o in models.Category.objects.all()])

class BidProd(forms.ModelForm):
    class Meta:
        model = models.BidDetails
        exclude = ['bid_time']
        widgets = {'name':forms.HiddenInput()}

class Comment(forms.ModelForm):
    class Meta:
        model = models.Comments
        widgets = {'comment':forms.Textarea(),'name':forms.HiddenInput()}

class EditUser(forms.ModelForm):
    class Meta:
        model = models.UserModel()
        exclude = ['role']
class ApproveUser(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['verified']
class BanUser(forms.ModelForm):
    class Meta:
        model = models.UserModel()
        fields = ['banned']
class CatMan(forms.ModelForm):
    class Meta:
        model = models.CatMan
class Appoint(forms.Form):
    name =forms.ChoiceField()
    def __init__(self,*args,**kwargs):
        super(Appoint,self).__init__(*args,**kwargs)
        self.fields['name']=forms.ChoiceField(choices=[(o.username,str(o)) for o in models.UserModel.objects.filter(role='F')])
    #class Meta:
        #model =models.Category
     #   fields= ['manager_name']
    #cat =forms.ChoiceField(choicess=([('0','all')].__add__(list(models.UserModel.objects.values_list('id','username'))))
class VerifyProduct(forms.ModelForm):
    class Meta:
        model = models.Products()
        fields = ['valid']
