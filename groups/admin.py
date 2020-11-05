from django.contrib import admin

from groups.models import Groups, GroupRelationship
# Register your models here.
admin.site.register(Groups)
admin.site.register(GroupRelationship)