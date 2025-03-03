import json

from . models import Coupon
from django_redis import get_redis_connection


def get_coupon_list(user_id):
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


def get_available_coupons(user_id):
    pass
