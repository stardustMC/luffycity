import json
from datetime import datetime
from .services import add_coupon_to_redis
from django.contrib import admin
from django_redis import get_redis_connection

from .models import Coupon, CouponDirection, CouponCourseCat, CouponCourse, CouponLog


# Register your models here.
class CouponDirectionInLine(admin.TabularInline):  # admin.StackedInline
    """学习方向的内嵌类"""
    model = CouponDirection
    fields = ["id", "direction"]


class CouponCourseCatInLine(admin.TabularInline):  # admin.StackedInline
    """课程分类的内嵌类"""
    model = CouponCourseCat
    fields = ["id", "category"]


class CouponCourseInLine(admin.TabularInline):  # admin.StackedInline
    """课程信息的内嵌类"""
    model = CouponCourse
    fields = ["id", "course"]


class CouponModelAdmin(admin.ModelAdmin):
    """优惠券的模型管理器"""
    list_display = ["id", "name", "start_time", "end_time", "total", "has_total", "coupon_type", "get_type", ]
    inlines = [CouponDirectionInLine, CouponCourseCatInLine, CouponCourseInLine]


admin.site.register(Coupon, CouponModelAdmin)


class CouponLogModelAdmin(admin.ModelAdmin):
    """优惠券发放和使用日志"""
    list_display = ["id", "user", "coupon", "order", "use_time", "use_status"]

    def save_model(self, request, obj, form, change):
        obj.save()
        # store coupon log in redis
        redis = get_redis_connection("coupon")
        hkey = "%s:%s" % (obj.id, obj.user.id)
        if obj.use_status == 0 and obj.use_time is None:
            add_coupon_to_redis(obj)
        else:
            redis.hdel(hkey)

    def delete_model(self, request, obj):
        redis = get_redis_connection("coupon")
        redis.hdel("%s:%s" % (obj.id, obj.user.id))
        obj.delete()

    def delete_queryset(self, request, queryset):
        redis = get_redis_connection("coupon")
        for obj in queryset:
            redis.hdel("%s:%s" % (obj.id, obj.user.id))
        queryset.delete()


admin.site.register(CouponLog, CouponLogModelAdmin)