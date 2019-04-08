from django.contrib import admin
from blogs.models import UserInfo
from .models import User
# Register your models here.


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    # fields = ('u', 'company', 'position', 'sh')
    # readonly_fields = ['u', 'realName']
    exclude = []
    list_display = ['u', 'company', 'position', 'realName', 'sh']
    list_editable = ['sh']
    list_per_page = 5
    list_filter = ['sh']
