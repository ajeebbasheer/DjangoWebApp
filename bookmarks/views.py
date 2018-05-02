# Create your views here.
from xdg.Locale import update
from django.contrib.auth import authenticate
from django.http import Http404,HttpResponse
from django import template
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms
from forms import LoginForm
from forms import SignUp
from forms import PlaceAdd
from forms import AddCat
from forms import Search
from forms import BidProd
from forms import Comment
from forms import Login
from forms import EditUser
from forms import ApproveUser
from forms import BanUser
from forms import CatMan
from forms import Appoint
from forms import VerifyProduct
import models
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
import datetime
from web_app import settings

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form = SignUp()
        return render(request,'signup.html', {'form': form})

    def post(self,request):
        form = SignUp(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data['password']
            p2 = form.cleaned_data['password1']
            if p1 != p2:
                return render(request, 'signup.html', {'form': form, 'error': True})
                #raise form.ValidationError("passwords do not match!!!")
            else:
                form.save()
                return HttpResponseRedirect('/thanks1/')
        #request.POST['password']=''
        return render(request,'signup.html',{'form':form})

class ThanksView1(View):
    def get(self,request):
        f=SignUp(request.POST)
        k='Your Registration is Succesfull!!,please wait for approval'
        return render(request,'back.html', {'msg':k,'value':'back'})
    def post(self,request):
        if request.method == 'POST':
            return HttpResponseRedirect('/signup/')


class ThanksView2(View):
    def get(self,request):
        f=AddCat(request.POST)
        k='successfully added a category!!'
        return render(request,'back.html', {'msg':k,'value':'add another category'})
    def post(self,request):
        if request.method == 'POST':
            return HttpResponseRedirect('/addcat/')

class ThanksView3(View):
    def get(self,request):
        f=AddCat(request.POST)
        k='successfully added a product!!..wait for approval..'
        return render(request,'back.html', {'msg':k,'value':'add another product'})
    def post(self,request):
        if request.method == 'POST':
            return HttpResponseRedirect('/placeadd/')

class LoginPageView(View):
    def get(self,request):
        k='u r success fullykk logged in!!'
        return render(request,'back.html', {'form':k,'value':'go back'})
    def post(self,request):
        if request.method == 'POST':
            return HttpResponseRedirect('/placeadd/')


###################### LOGIN FUNCTION -LOGIN AS CUSTOMER,CAT_MANAGER AND ADMIN #########################################

class LoginView(View):
    def get(self,request):
        form = Login()
        return render(request,'base.html',{'form':form,'title':'loginpage','head':'LOGIN','value':'login'})
    def post(self,request):
        if request.method == 'POST':
            form = Login(request.POST)

            if form.is_valid():#CHECKING WHETHER ANY FIELDS ARE BLANK AND TYPE MISMATCHES
                #GETTING DATA ENTERED IN FORM
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                #u can use request.POST instead of form.cleaned_data
                print '%s %s' %(username,password)
                p = models.UserModel.objects.login(username,password)#
                q = models.UserModel.objects.logincust(username)
                r = models.UserModel.objects.loginman(username)
                s = models.UserModel.objects.loginadmin(username)
                t = models.UserModel.objects.loginban(username)
                u = models.UserModel.objects.loginapprove(username)
                if not t:
                    if p:                                                   #CHECK USERNAME AND PASSWORD MATCH
                        request.session['name']=username
                        if q:                                               #IF NORMAL USER
                            if s:                                           #IF ADMIN(HERE SET ADMIN AS NORMAL USER)
                                return HttpResponseRedirect('/adminhome/')
                            elif u:
                                return HttpResponseRedirect('/userhome/')   #LOGIN FOR NORMAL USERS EXCEPT ADMIN
                            else:
                                return render(request,'base2.html',{'marquee_text':'YOUR REGSTRATION IS SUCCESSFULL!!!....PLEASE WAIT FOR APPROVAL'})
                        if r:                                               #LOGIN FOR MANAGER
                            if u:
                                return HttpResponseRedirect('/manhome/')
                            else:
                                return render(request,'base2.html',{'marquee_text':'YOUR REGSTRATION IS SUCCESSFULL!!!....PLEASE WAIT FOR APPROVAL'})
                    else:
                        return render(request,'base.html',{'form':form,'title':'loginpage','head':'LOGIN','value':'login',
                    'error':True,'error_msg':'username does not exist!!!'}) #IF USERNAME DOES NOT EXISTS
                else:
                    return render(request,'base.html',{'form':form,'title':'loginpage','head':'LOGIN','value':'login',
                    'error':True,'error_msg':'SORRY YOU ARE BANNED BY ADMIN..!!!'})
            return render(request,'base.html',{'form':form,'head':'LOGIN','value':'login', 'error':True,'error_msg':'invalid login!!!'})

#-----------------------------------------------------------------------------------------------------------------------
################################## LOGOUT##############################################################################
class LogoutView(View):
    def get(self,request):
        request.session.flush()
        return HttpResponseRedirect('/login/')
#-----------------------------------------------------------------------------------------------------------------------

################  HOME PAGES OF CUSTOMER,CAT_MANAGER AND ADMIN #########################################################


class UserPageView(View):
    def get(self,request):
        print request.session.get('name')
        k=request.session.get('name')
        return render(request,'cust_home.html',{'title':'MainPage','head':k,
                'url_1':'/placeadd/','url_2':'/bidprod/','link_text_1':'Place Advertisement','link_text_2':'Bid Product',
                'url_3':'/search/','link_text_3':'Search Product','url_4':'/delete/','link_text_4':'Delete Product',
                'url_5':'/comment/','link_text_5':'Comment Product'})

class AdminPageView(View):
    def get(self,request):
        print request.session.get('name')
        return render(request,'admin_home.html',{'title':'adminPage','head':'Welcome Administrator..',
                'url_1':'/showall/','url_2':'/unapproved/','link_text_1':'User Details','link_text_2':'Approve User',
                'url_3':'/unbanned/','link_text_3':'Ban User','url_4':'/addcat/','link_text_4':'Add Category',
                'url_5':'/catview/','link_text_5':'appoint Category manager'})

class ManagerPageView(View):
    def get(self,request):
        print request.session.get('name')
        k=request.session.get('name')
        return render(request,'man_home.html',{'title':'manager Page','head':k,
                'url_1':'/productview/','link_text_1':'approve products'})

##----------------------------------------------------------------------------------------------------------------------
############################### DISPLAY USER DETAILS ###################################################################
class DisplayView(View):
    def get(self,request):
        m= models.UserModel.objects.showall()
        return render(request,'showall.html',{'users':m,'head':'List of Users...'})
#-----------------------------------------------------------------------------------------------------------------------
################################# DELETE VIEW ##########################################################################
class DeleteView(View):
    def get(self,request):
        name = request.session.get('name')
        user = models.UserModel.objects.get(username=name) #get current object
        ownproducts = models.Products.objects.findownprodect(user)
        return render(request,'showproduct.html',{'products':ownproducts,'head':'your products'})
class DeletedView(View):
    def get(self,request,prodid):
        prod = models.Products.objects.get(pk=prodid)
        del_item = prod.product_name
        return render(request,'delete.html',{'delete':del_item,'value':'delete'})
    def post(self,request,prodid):
        prod = models.Products.objects.get(pk=prodid)
        prod.delete()
        return HttpResponseRedirect('/userhome/')


    def post(self,request,prodid):
        prod = models.Products.objects.get(pk=prodid) #prodid passed from url..get data from url
        prod.delete()


#-----------------------------------------------------------------------------------------------------------------------
#class n(form.Form)
#cat =forms.ChoiceField(choicess=([('0','all')].__add__(list(Category.objects.values_list('id','name'))))



#
#self.filter((Q(name__icontains=keyw)|Q.......
class EditView(View):
    def get(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = EditUser(instance=user)   #makes an instance of the Editform for user with pk=userid.
        p = user.first_name
        return render(request,'base.html',{'form':form1,'head':p,'value':'save changes'})
    def post(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = EditUser(request.POST,instance = user)
        p = user.first_name
        if form1.is_valid():
            form1.save()
        return render(request,'base.html',{'form':form1,'head':p,'value':'save changes'})

#----------------------------------------------------------------------------------------------------------------------
################################### APPROVE USER #######################################################################
class UnapprovedView(View):
    def get(self,request):
        m= models.UserModel.objects.approve()
        return render(request,'showall.html',{'users':m,'head':'Pending Requests...'})
#---------------------------------------------------------


class ApproveView(View):
    def get(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = ApproveUser(instance=user)   #makes an instance of the Editform for user with pk=userid.
        p = user.first_name
        return render(request,'base.html',{'form':form1,'head':p,'value':'save changes'})
    def post(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = ApproveUser(request.POST,instance = user)
        m= models.UserModel.objects.approve()
        p = user.first_name
        if form1.is_valid():
            form1.save()
            return HttpResponseRedirect('/adminhome/')
        return render(request,'showall.html',{'users':m,'head':'Pending Requests...'})



#-----------------------------------------------------------------------------------------------------------------------
################################### BAN USER ###########################################################################

class UnBannedView(View):
    def get(self,request):
        m= models.UserModel.objects.showall()
        return render(request,'showall.html',{'users':m})
#---------------------------------------------------------


class BannedView(View):
    def get(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = BanUser(instance=user)   #makes an instance of the Editform for user with pk=userid.
        p = user.first_name
        return render(request,'ban.html',{'form':form1,'head':p,'value':'save changes'})
    def post(self,request,userid):
        user = models.UserModel.objects.get(pk=userid)
        form1 = BanUser(request.POST,instance = user)
        p = user.first_name
        if form1.is_valid():
            form1.save()
            return HttpResponseRedirect('/adminhome/')
        return render(request,'ban.html',{'form':form1,'head':p,'value':'save changes'})
#-----------------------------------------------------------------------------------------------------------------------
################################# Appoint Category Manager #######################################################################
class CatView(View):
    def get(self,request):
        m = models.Category.objects.showall()
        return render(request,'showcat.html',{'cats':m})
class AppointCat(View):
    def get(self,request,catid):
        cat = models.Category.objects.get(pk=catid)
        form = Appoint()
        p = cat.category_name
        return render(request,'appoint.html',{'form':form,'head':p,'value':'appoint'})
    def post(self,request,catid):
        cat = models.Category.objects.get(pk=catid)
        form = Appoint(request.POST)
        p = cat.category_name
        if form.is_valid():
            u=models.UserModel.objects.get(username=form.cleaned_data['name'])
            cat.manager_name=u
            cat.save()
            return HttpResponseRedirect('/adminhome/')
        return render(request,'appoint.html',{'form':form,'head':p,'value':'appoint'})

#----------------------------------------------------------------------------------------------------------------------
################################## Approve Product ####################################################################
class UnapprovedProductView(View):
    def get(self,request):
        m= models.Products.objects.unapprovedproduct()
        return render(request,'showproduct.html',{'products':m,'head':'Pending product requests..'})

class ApprovedView(View):
    def get(self,request,prodid):
        prod = models.Products.objects.get(pk=prodid)
        form1 = VerifyProduct(instance=prod)
        p = prod.product_name
        return render(request,'base.html',{'form':form1,'head':p,'value':'save changes'})
    def post(self,request,prodid):
        user = models.Products.objects.get(pk=prodid)
        form1 = VerifyProduct(request.POST,instance = user)
        m= models.Products.objects.unapprovedproduct()
        if form1.is_valid():
            form1.save()
            return HttpResponseRedirect('/manhome/')
        return render(request,'showproduct.html',{'products':m,'head':'Pending Product Requests...'})

#-----------------------------------------------------------------------------------------------------------------------
################################ BID VIEW ##############################################################################
class BidView(View):
    def get(self,request):
        form = BidProd()
        return render(request,'base.html',{'form':form,'head':'Bid Product','value':'bid'})
    def post(self,request):
        form = BidProd(request.POST)
        if form.is_valid():
            prod = form.cleaned_data['Product']
            quant = form.cleaned_data['bid_quantity']
            amnt = form.cleaned_data['bid_amount']
            p = models.Products.objects.check_bid_quantity(quant,prod)
            q = models.Products.objects.check_minbid(amnt,prod)
            if p:
                if q:
                    username = request.session.get('name') #get curent user name,since it is set as unique,we can use
                    print username  #to print current user at command line
                    user =models.UserModel.objects.get(username=username)

                    bid = form.save(commit=False)
                    bid.name = user
                    bid.save()
                    return HttpResponse("ok!")
                else:
                    return render(request,'base.html',{'form':form,'head':'Bid Product','value':'bid','error':True,'error_msg':'amount is very less!'})
            else:
                return render(request,'base.html',{'form':form,'head':'Bid Product','value':'bid','error':True,'error_msg':'required amount is not available!'})
        else:
            return render(request,'base.html',{'form':form,'head':'Bid Product','value':'bid','error':True,'error_msg':'invalid entries..!'})

#------------------------------------------------------------------------------------------------------------------------------------
########################################## search ###################################################################################
class SearchView(View):
    def get(self,request):
        form = Search()
        return render(request,'base.html',{'form':form,'title':'search','head':'search','value':'search'})
    def post(self,request):
        form = Search(request.POST)
        if form.is_valid():
            cat_name = form.cleaned_data['category']
            key = form.cleaned_data['enter_keyword']
            p = models.Products.objects.searchall(key)
            q = models.Products.objects.searchcat(key,cat_name)
            if cat_name =='0':
                return render(request,'showproduct.html',{'products':p,'media_url':settings.MEDIA_URL})
            else:
                return render(request,'showproduct.html',{'products':q,'media_url':settings.MEDIA_URL})
        return render(request,'base.html',{'form':form,'title':'search','head':'search','value':'search'})

#-------------------------------------------------------------------------------------------------------------------------------------
########################################## comment ###################################################################################
class CommentView(View):
    def get(self,request):
        form = Comment()
        return render(request,'base.html',{'form':form,'title':'comments','head':'Add your Comments','value':'add comment'})
    def post(self,request):
        form = Comment(request.POST)
        if form.is_valid():
            name = request.session.get('name')
            user = models.UserModel.objects.get(username=name)
            comment=form.save(commit=False) #form will not save now,instead an object creates (comment)..this is to save the hidden
            comment.name = user
            comment.save()
            return HttpResponseRedirect('/userhome/')
        return render(request,'base.html',{'form':form,'title':'comments','head':'Add your Comments','value':'add comment'})
                                            #input data..and one more advantage is it if it was saved by form.save it will show integrity
                                            #error..so we fill the hidden column and then save.

#-----------------------------------------------------------------------------------------------------------------------------------
###################################### PLACE ADD #################################################################################

class PlaceAddView(View):
    def get(self,request):
        form = PlaceAdd();
        return render(request,'base.html',{'form':form,'title':'place add','head':'Place Advertisement','value':'add'})
    def post(self,request):
        form = PlaceAdd(request.POST,request.FILES)
        if form.is_valid():
            name = request.session.get('name')
            user = models.UserModel.objects.get(username=name)
            add = form.save(commit=False)
            add.name = user
            add.save()
            return HttpResponseRedirect('/thanks3/')
        else:
            print settings.MEDIA_URL
            return render(request,'base.html',{'form':form,'title':'place add','head':'Place Advertisement','value':'add','media_url':settings.MEDIA_URL})

#-------------------------------------------------------------------------------------------------------------------------
class AddCatView(View):
    def get(self,request):
        form = AddCat()
        return render(request,'base.html',{'form':form,'title':'add cat','head':'Add Category','value':'add'})
    def post(self,request):
        form = AddCat(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks2/')
        else:
            return render(request,'base.html',{'form':form,'title':'Add Cat','head':'Add Category','value':'add'})



def login(request):
    form = LoginForm()
    return render(request,'base.html',{'form':form,'title':'loginpage','head':'LOGIN','value':'login'})
def signup(request):
    form = SignUp()
    return render(request,'signup.html', {'form': form})

def placeadd(request):
    form = PlaceAdd()
    return render(request,'placeadd.html',{'form':form})
def addcat(request):
    form = AddCat()
    return render(request,'addcat.html',{'form':form})

def search(request):
    form = Search()
    return render(request,'searchby.html',{'form':form,'value':'search'})

def bidprod(request):
    form = BidProd()
    return render(request,'bidprod.html',{'form':form})

def comment(request):
    form = Comment()
    return render(request,'base.html',{'form':form,'title':'comments','head':'Add your Comments','value':'add comment'})

def login(request):
    c = {}
    c = update(csrf(request))
    return render_to_response(login.html)
