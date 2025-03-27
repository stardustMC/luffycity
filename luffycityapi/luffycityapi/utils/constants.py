"""significant constants that define the web page"""
# 导航的位置 --> 顶部
NAV_HEADER_POSITION = 0
# 导航的位置 --> 脚部
NAV_FOOTER_POSITION = 1
# 顶部导航显示的最大数量
NAV_HEADER_SIZE = 5
# 脚部导航显示的最大数量
NAV_FOOTER_SIZE = 10
# maximum number of carousel
BANNER_SIZE = 10
# list page cache period
LIST_PAGE_CACHE_TIME = 60 * 60

# 设置热门搜索关键字在redis中的key前缀名称
DEFAULT_HOT_WORD = "hot_words"
# 设置返回的热门搜索关键字的数量
HOT_WORD_LENGTH = 5
# 设置热门搜索关键字的有效期时间[单位：天]
HOT_WORD_EXPIRE = 7

# 积分抵扣现金的比例 10:1
CREDIT_TO_DISCOUNT_PRICE = 10
# 订单支付时间
ORDER_EXPIRE_TIME = 15 * 60

# 订单每页展示数量
ORDER_PAGE_SIZE = 5