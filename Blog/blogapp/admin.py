from django.contrib import admin
from blogapp.models import CustomUser , Categories , Post ,Comment , Contact



@admin.register(Contact)
class ContactAmin(admin.ModelAdmin):
    list_display = ['name','email','subject','message']


@admin.register(CustomUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display=['id','email','first_name','last_name','phone','is_active','img']
    readonly_fields = ['password','date_joined','last_login','is_staff','is_superuser','is_active']


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'author', 'categories', 'video', 'picture', 'created_at', 'updated_at']




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post','author','content','created_at']



