from django.contrib import admin

# Register your models here.
# class TestModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'goods_detail']
#
from apps.users.models import User

admin.site.register(User)

