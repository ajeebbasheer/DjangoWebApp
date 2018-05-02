#of fields to display on change-list pages. Edit admin.py to make these changes:
from django.contrib import admin
from bookmarks.models import UserModel,Products,Category,Comments,BidDetails
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city')
    search_fields = ('name',)
class studentAdmin(admin.ModelAdmin):
    list_display = ('name','roll')
    list_filter = ('roll',)
class booksAdmin(admin.ModelAdmin):
    list_display = ('title','pubdate','publisher')
    list_filter =  ('pubdate',)
    filter_horizontal = ('authors',)
#admin.site.register(Publisher, PublisherAdmin)
#admin.site.register(student, studentAdmin)
#admin.site.register(books, booksAdmin)
#admin.site.register(Customer)
#admin.site.register(Products)
admin.site.register(UserModel)
admin.site.register(Category)
admin.site.register(BidDetails)
admin.site.register(Comments)
admin.site.register(Products)
