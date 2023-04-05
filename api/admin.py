from django.contrib import admin

from api.models import User, Operation, Record

class UserAdmin(admin.ModelAdmin):
    pass

class OperationAdmin(admin.ModelAdmin):
    pass

class RecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Record, RecordAdmin)