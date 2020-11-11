from django.contrib import admin
from server.models import Profile


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    用户信息后台配置
    """
    list_display = ('uid', 'user_status', 'user_type', 'account', 'user_level', 'name',
                    'phone', 'city', 'cert_type', 'cert_number', 'introduction')
    list_filter = ('user_status', 'user_level', 'city')
    search_fields = ('account', 'name', 'phone')
    readonly_fields = ('uid', 'user_status', 'user_type', 'account', 'user_level', 'name',
                       'city', 'cert_type', 'cert_number')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = ['uid']
        return self.readonly_fields
