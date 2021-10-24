from django.contrib import admin

from user.models import User, Following, BlockList

admin.site.register(User)
admin.site.register(Following)
admin.site.register(BlockList)
