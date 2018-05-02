from django.conf.urls.defaults import *
from bookmarks import views
#from bookmarks import views
#from bookmarks import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#from web_app.bookmarks.views import dt

urlpatterns = patterns('',
    (r'^login/$',views.LoginView.as_view()),
    (r'^logout/$',views.LogoutView.as_view()),
    (r'^signup/$',views.SignUpView.as_view()),
    (r'^placeadd/$',views.PlaceAddView.as_view()),
    (r'^addcat/$',views.AddCatView.as_view()),
    (r'^search/$',views.SearchView.as_view()),
    (r'^delete/$',views.DeleteView.as_view()),
    (r'^delete/(?P<prodid>\d+)/$',views.DeletedView.as_view()),
    (r'^bidprod/$',views.BidView.as_view()),
    (r'^comment/$',views.CommentView.as_view()),
    (r'^thanks1/$',views.ThanksView1.as_view()),
    (r'^thanks2/$',views.ThanksView2.as_view()),
    (r'^thanks3/$',views.ThanksView3.as_view()),
    (r'^loginpage/$',views.LoginPageView.as_view()),
    (r'^userhome/$',views.UserPageView.as_view()),
    (r'^adminhome/$',views.AdminPageView.as_view()),
    (r'^manhome/$',views.ManagerPageView.as_view()),
    (r'^showall/$',views.DisplayView.as_view()),
    (r'^showall/(?P<userid>\d+)/$',views.EditView.as_view()),
    (r'^unapproved/$',views.UnapprovedView.as_view()),
    (r'^unapproved/(?P<userid>\d+)/$',views.ApproveView.as_view()),
    (r'^unbanned/$',views.UnBannedView.as_view()),
    (r'^unbanned/(?P<userid>\d+)/$',views.BannedView.as_view()),
    (r'^catview/$',views.CatView.as_view()),
    (r'^catview/(?P<catid>\d+)/$',views.AppointCat.as_view()),
    (r'^productview/$',views.UnapprovedProductView.as_view()),
    (r'^productview/(?P<prodid>\d+)/$',views.ApprovedView.as_view()),


    #(r'^url1/$',views.login),
   # (r'^url1/$',views.loggedin),
  #  (r'^url1/$',views.auth_view),
 #   (r'^url1/$',views.invalid_login),
#    (r'^url1/$',views.logout),

    (r'^admin/', include(admin.site.urls)),
)


#user= models....get(pk=uid)
#f1=forms.form(instance=user)