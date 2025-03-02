import json
from datetime import datetime

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
            pipe = redis.pipeline()
            pipe.multi()
            pipe.hset(hkey, "coupon_id", obj.coupon.id)
            pipe.hset(hkey, "name", obj.coupon.name)
            pipe.hset(hkey, "discount", obj.coupon.discount)
            pipe.hset(hkey, "get_discount_display", obj.coupon.get_discount_display())
            pipe.hset(hkey, "coupon_type", obj.coupon.coupon_type)
            pipe.hset(hkey, "get_coupon_type_display", obj.coupon.get_coupon_type_display())
            pipe.hset(hkey, "start_time", obj.coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(hkey, "end_time", obj.coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
            pipe.hset(hkey, "get_type", obj.coupon.get_type)
            pipe.hset(hkey, "get_get_type_display", obj.coupon.get_get_type_display())
            pipe.hset(hkey, "condition", obj.coupon.condition)
            pipe.hset(hkey, "sale", obj.coupon.sale)
            pipe.hset(hkey, "to_direction",
                      json.dumps(list(obj.coupon.to_direction.values("direction__id", "direction__name"))))
            pipe.hset(hkey, "to_category",
                      json.dumps(list(obj.coupon.to_category.values("category__id", "category__name"))))
            pipe.hset(hkey, "to_course",
                      json.dumps(list(obj.coupon.to_course.values("course__id", "course__name"))))
            pipe.expire(hkey, obj.coupon.endtime.timestamp() - datetime.now().timestamp())
            pipe.execute()
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