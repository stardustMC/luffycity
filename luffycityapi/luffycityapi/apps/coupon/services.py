import json
from . models import Course
from datetime import datetime
from django_redis import get_redis_connection


def get_coupon_list(user_id: int):
    redis = get_redis_connection("coupon")
    coupon_hkeys = redis.keys("*:%s" % user_id)
    try:
        coupon_hkeys = [key.decode("utf-8") for key in coupon_hkeys]
    except:
        coupon_hkeys = []

    coupon_list = []
    for hkey in coupon_hkeys:
        coupon_id = hkey.split(":")[0]
        coupon_hash = redis.hgetall(hkey)
        coupon = {}
        for key, value in coupon_hash.items():
            key = key.decode()
            value = value.decode()
            if key in ["to_direction", "to_category", "to_course"]:
                value = json.loads(value)
            coupon[key] = value
        coupon["id"] = coupon_id
        coupon_list.append(coupon)
    return coupon_list


def get_available_coupons(user_id: int):
    redis = get_redis_connection("cart")
    cart_hash = redis.hgetall("cart_%s" % user_id)
    selected_id_list = {int(cid.decode()) for cid, select in cart_hash.items() if select == b'1'}
    courses = Course.objects.filter(pk__in=selected_id_list, is_deleted=False, is_show=True).all()

    category_id_list, direction_id_list = set(), set()
    for course in courses:
        # 获取被勾选的商品课程的父类课程分类id列表，并保证去重
        category_id_list.add(int(course.category.id))
        # # 获取被勾选的商品课程的父类学习方向id列表，并保证去重
        direction_id_list.add(int(course.direction.id))

    coupons = get_coupon_list(user_id)
    avail_coupons = []
    for coupon in coupons:
        coupon_type = int(coupon["coupon_type"])
        # general used coupon
        if coupon_type == 0:
            coupon["avail_courses"] = "__all__"
            avail_coupons.append(coupon)
        # direction specified
        elif coupon_type == 1:
            include_directions = {int(item["direction__id"]) for item in coupon["to_direction"]}
            ret = include_directions & direction_id_list
            include_id_set = {course.id for course in courses if course.direction_id in ret}
            if ret:
                coupon["avail_courses"] = include_id_set
                avail_coupons.append(coupon)
        # category specified
        elif coupon_type == 2:
            include_categories = {int(item["category__id"]) for item in coupon["to_category"]}
            ret = include_categories & category_id_list
            include_id_set = {course.id for course in courses if course.category_id in ret}
            if ret:
                coupon["avail_courses"] = include_id_set
                avail_coupons.append(coupon)
        # course specified
        elif coupon_type == 3:
            include_courses = {int(item["course__id"]) for item in coupon["to_course"]}
            ret = include_courses & selected_id_list
            if ret:
                coupon["avail_courses"] = ret
                avail_coupons.append(coupon)
    return avail_coupons


def add_coupon_to_redis(coupon_log):
    # store coupon log in redis
    redis = get_redis_connection("coupon")
    hkey = "%s:%s" % (coupon_log.coupon.id, coupon_log.user.id)
    pipe = redis.pipeline()
    pipe.multi()
    pipe.hset(hkey, "coupon_id", coupon_log.coupon.id)
    pipe.hset(hkey, "name", coupon_log.coupon.name)
    pipe.hset(hkey, "discount", coupon_log.coupon.discount)
    pipe.hset(hkey, "get_discount_display", coupon_log.coupon.get_discount_display())
    pipe.hset(hkey, "coupon_type", coupon_log.coupon.coupon_type)
    pipe.hset(hkey, "get_coupon_type_display", coupon_log.coupon.get_coupon_type_display())
    pipe.hset(hkey, "start_time", coupon_log.coupon.start_time.strftime("%Y-%m-%d %H:%M:%S"))
    pipe.hset(hkey, "end_time", coupon_log.coupon.end_time.strftime("%Y-%m-%d %H:%M:%S"))
    pipe.hset(hkey, "get_type", coupon_log.coupon.get_type)
    pipe.hset(hkey, "get_get_type_display", coupon_log.coupon.get_get_type_display())
    pipe.hset(hkey, "condition", coupon_log.coupon.condition)
    pipe.hset(hkey, "sale", coupon_log.coupon.sale)
    pipe.hset(hkey, "to_direction",
              json.dumps(list(coupon_log.coupon.to_direction.values("direction__id", "direction__name"))))
    pipe.hset(hkey, "to_category",
              json.dumps(list(coupon_log.coupon.to_category.values("category__id", "category__name"))))
    pipe.hset(hkey, "to_course",
              json.dumps(list(coupon_log.coupon.to_course.values("course__id", "course__name"))))
    pipe.expire(hkey, int(coupon_log.coupon.end_time.timestamp() - datetime.now().timestamp()))
    pipe.execute()