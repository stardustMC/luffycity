import http from "../utils/http";
import {reactive} from "vue";

const order = reactive({
    total_price: 0,         // 勾选商品的总价格
    use_coupon: false,      // 用户是否使用优惠
    discount_type: 0,       // 0表示优惠券，1表示积分
    discount_price: 0,
    avail_coupon_list: [],  // 用户可用优惠券列表
    coupon_list: [],        // 用户拥有的所有优惠券列表
    select: -1,             // 当前用户选中的优惠券下标，-1表示没有选择
    fixed: true,            // 底部订单总价是否固定浮动
    pay_type: 0,            // 支付方式

    credit: 0,              // 当前用户选择抵扣的积分，0表示没有使用积分
    credit_ratio: 0,         // 积分换算比例
    own_credit: 0,          // 用户拥有积分
    max_use_credit: 0,         // 最多可用积分
    avail_credit_list: [],     // 可用积分的课程

    course_list: [],        // 购买的课程列表
    show_success: false,    // 是否展示支付成功页面
    real_price:  0,         // 实付金额
    deal_time: undefined,   // 交易时间

    create_order(user_coupon_id, token) {
        // 生成订单
        return http.post("/orders/", {
            user_coupon_id: user_coupon_id,
            pay_type: this.pay_type,
            discount_type: this.discount_type
        }, {
            headers: {
                Authorization: "jwt " + token,
            }
        })
    },
    get_user_coupons(token) {
        return http.get("/coupons/", {
            headers: {
                Authorization: "jwt " + token,
            }
        })
    },
    get_order_avail_coupons(token) {
        return http.get("/coupons/avail/", {
            headers: {
                Authorization: "jwt " + token,
            }
        })
    },
    alipay_page_pay(order_number){
        return http.get(`payment/alipay/${order_number}`);
    },
    alipay_post_display(query_string){
        return http.get(`payment/alipay/result/${query_string}`);
    }
})

export default order;