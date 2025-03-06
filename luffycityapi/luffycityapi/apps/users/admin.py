from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, _
from .models import User, Credit


# Register your model here
class UserModelAdmin(UserAdmin):
    list_display = ["id", "username", "avatar_small", "money", "credit", "mobile"]
    # fieldsets 和 add_fieldsets 都在从UserAdmin中复制粘贴过来，重写加上自己需要的字段的。
    fieldsets = (
        (None, {'fields': ('username', 'password', 'credit', 'avatar')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        # 若更新数据
        if change:
            user = User.objects.get(id=obj.id)
            old_credit = user.credit
            new_credit = obj.credit

            Credit.objects.create(
                operation=2,
                user=user,
                number=int(new_credit - old_credit),
            )
        obj.save()

        # 若新增用户
        if not change:
            Credit.objects.create(
                operation=2,
                user=obj.id,
                number=obj.credit,
            )

admin.site.register(User, UserModelAdmin)

class CreditModelAdmin(admin.ModelAdmin):
    list_display = ['id', "user", "number", "__str__", "remark"]

admin.site.register(Credit, CreditModelAdmin)