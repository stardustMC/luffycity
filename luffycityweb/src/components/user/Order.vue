<template>
      <div class="right-container l">
        <div class="right-title">
          <h2>我的订单</h2>
          <ul>
            <li :class="{action:orders.status===-1}">
              <router-link to="/user/order" @click.prevent="orders.status=-1">
                全部<i class="js-all-num" v-if="orders.status === -1">{{orders.count}}</i>
              </router-link>
            </li>

            <li v-for="choice in orders.order_status_choices" :class="{action:choice[0]===orders.status}">
              <router-link to="/user/order?type=unpaid" @click.prevent="orders.status=choice[0]">
                {{choice[1]}}<i class="js-all-num" v-if="orders.status===choice[0]">{{orders.count}}</i>
              </router-link>
            </li>
          </ul>
        </div>
        <div class="myOrder">
          <ul class="myOrder-list">
            <li :data-flag="order.order_number" v-for="order in orders.order_list">
              <p class="myOrder-number">
                <i class="imv2-receipt"></i>订单编号：{{order.order_number}}
                <span class="date">{{order.created_time.toString().replace("T", " ").split(".")[0]}}</span>
                <i class="imv2-delete js-order-del" title="删除订单"></i>
                <router-link to="/user/help" target="_blank" class="myfeedback r">售后帮助</router-link>
              </p>
              <div class="myOrder-course clearfix" v-for="course in order.order_courses">
                <dl class="course-del l">
                  <dd class="clearfix">
                    <router-link :to="`/project/${course.course_id}`" class="l"><img class="l" :src="course.course_cover" width="160" height="90"></router-link>
                    <div class="del-box l">
                      <!-- type为类型 1实战购买 2实战续费 4就业班购买 5就业班续费 -->
                      <!-- cate 订单类型 0无优惠 1组合套餐 2学生优惠 -->
                      <router-link :to="`/project/${course.course_id}`"><p class="course-name">{{course.course_name}}</p></router-link>
                      <p class="price-btn-box clearfix">
                        <!-- 如果有优惠券 -->
                        <span class="l truepay-text">实付</span>
                        <span class="l course-little-price">￥{{order.real_price}}</span>
                      </p>
                    </div>
                  </dd>
                </dl>
                <!-- 使用优惠券 -->
                <div class="course-money l pt15">
                  <div class="wrap">
                    <div class="type-box clearfix mb10">
                      <p class="type-text l">原价</p>
                      <p class="type-price l line-though"><span class="RMB">¥</span>{{order.total_price}}</p>
                    </div>
                    <div class="type-box clearfix mb10">
                      <p class="type-text l">折扣</p>
                      <p class="type-price l">-<span class="RMB">¥</span>{{order.total_price - order.real_price}}</p>
                    </div>
                    <div class="total-box clearfix">
                      <p class="type-text l">实付</p>
                      <p class="type-price l"><span class="RMB">¥</span>{{order.real_price}}</p>
                    </div>
                  </div>
                </div>
                <div class="course-action l" v-if="order.order_status === 0">
                  <a class="pay-now" href="" @click.prevent="pay_now(order)">立即支付</a>
                  <a class="order-cancel" href="" @click.prevent="pay_cancel(order)">取消订单</a>
                </div>
                <div class="course-action l" v-else-if="order.order_status === 1">
                  <a class="pay-now" href="" @click.prevent="evaluate_now(order)">立即评价</a>
                  <a class="order-cancel" href="" @click.prevent="order_refund(order)">申请退款</a>
                </div>
                <div class="course-action l" v-else-if="order.order_status === 2">
                  <a class="pay-now" href="" @click.prevent="delete_order(order)">删除订单</a>
                </div>
                <div class="course-action l" v-else-if="order.order_status === 3">
                  <a class="pay-now" href="" @click.prevent="recovery_now(order)">订单恢复</a>
                  <a class="pay-now" href="" @click.prevent="delete_order(order)">删除订单</a>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div class="page" style="text-align: center">
          <el-pagination
              background
              layout="sizes, prev, pager, next, jumper"
              :total="orders.count"
              :page-sizes="[5, 10, 15, 20]"
              :page-size="orders.size"
              :current-page=orders.page
              @current-change="current_page"
              @size-change="current_size"
          ></el-pagination>
        </div>
      </div>
</template>

<script setup>
import {order, orders} from "../../api/order.js";
import {ElMessage} from "element-plus";
import {watch} from "vue";
import router from "../../router/index.js";

const get_order_status_choices = () =>{
  orders.get_order_status_choices().then(response=>{
    orders.order_status_choices = response.data;
  })
};
get_order_status_choices();

const get_order_list = () =>{
  let token = localStorage.getItem("token") || sessionStorage.getItem("token");
  orders.get_order_list(token).then(response=>{
    orders.order_list = response.data.results;
    orders.count = response.data.count;
  })
}
get_order_list();

const pay_now = (order_info) =>{
  order.order_number = order_info.order_number;
  let token = localStorage.getItem("token") || sessionStorage.getItem("token");
  // 提交订单后，根据返回的订单号，跳转到支付页面
  order.alipay_page_pay(token).then(response => {
    clearInterval(order.timer);
    order.timeout = 180;
    order.timer = setInterval(() => {
      if (order.timeout > 1){
        order.timeout -= 1;
        order.query_order(token).then(response=>{
          order_info.order_status = 1;
          clearInterval(order.timer);
        }).catch(err=>{
          console.log(err.response.data);
        })
      } else {
        clearInterval(order.timer);
      }
    }, 8000)
    window.open(response.data.link, "_blank");
  })
}

const pay_cancel = (order_info)=>{
  // 取消订单
  let token = localStorage.getItem("token") || sessionStorage.getItem("token");
  orders.pay_cancel(token, order_info.id).then(response=>{
    if(response.status !== 200){
      ElMessage.error(response.data.errmsg);
    }else{
      let index = orders.order_list.findIndex(item => item===order_info);
      orders.order_list.splice(index, 1);
      ElMessage.success(response.data.errmsg);
    }
  })
}

const evaluate_now = (order_info)=>{
  // 订单评价
}

const order_refund = (order_info)=>{
  // 申请退款
}

const delete_order = (order_info)=>{
  // 删除订单
}

const recovery_now = (order)=>{
  // 恢复订单
}

// 切换页码
const current_page = (page)=>{
  orders.page = page;
}

// 切换分页数据量
const current_size = (size)=>{
  orders.size = size;
}

watch(()=>orders.status, ()=>{
  orders.page = 1;
  get_order_list();
})

// 监听页码
watch(
    ()=>orders.page,
    ()=>{
      get_order_list()
    }
)

// 监听页面数据量大小
watch(
    ()=>orders.size,
    ()=>{
      orders.page = 1;
      get_order_list()
    }
)
</script>

<style scoped>

.l {
    float: left;
}
.r {
    float: right;
}

.clearfix:after {
    content: '\0020';
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
}

/*****/
.right-container {
	width: 1284px;
}

.right-container .right-title {
	margin-bottom: 24px
}

.right-container .right-title::after {
	content: '';
	clear: both;
	display: block
}

.right-container .right-title h2 {
	margin-right: 24px;
	float: left;
	font-size: 16px;
	color: #07111b;
	line-height: 32px;
	font-weight: 700
}

.right-container .right-title ul {
	float: left
}

.right-container .right-title ul:before {
	float: left;
	margin-top: 2px;
	margin-right: 20px;
	content: "|";
	color: #d9dde1
}

.right-container .right-title ul li {
	float: left;
	width: 95px;
	line-height: 32px;
	text-align: center;
	font-size: 14px
}

.right-container .right-title ul li.action {
	background: #4d555d;
	border-radius: 16px
}

.right-container .right-title ul li.action a {
	color: #fff
}

.right-container .right-title ul li i {
	padding-left: 5px;
	font-style: normal
}

.right-container .right-title span {
	position: relative;
	float: right;
	color: #93999f;
	font-size: 14px;
	cursor: pointer;
	width: 128px;
	line-height: 32px
}

.right-container .right-title span i {
	float: left;
	margin-top: 8px;
	margin-left: 28px;
	margin-right: 4px;
	font-size: 16px
}

.right-container .right-title span a {
	display: block
}

.right-container .right-title span.action {
	background: #4d555d;
	border-radius: 16px
}

.right-container .right-title span.action a {
	color: #fff
}

.myOrder {
	width: 100%
}

.myOrder-list li {
	padding: 32px;
	padding-top: 0;
	box-shadow: 0 2px 8px 2px rgba(0,0,0,.1);
	margin-bottom: 24px;
	background: #fff;
	border-radius: 8px;
	position: relative
}

.myOrder-list li dd {
	margin-top: 24px;
	padding-top: 24px;
	position: relative;
	box-sizing: border-box;
	border-top: 1px solid #d9dde1
}

.myOrder-list li dd a {
	display: block
}

.myOrder-list li dd:first-child {
	border-top: none;
	margin-top: 0;
	padding-top: 0
}

.myOrder-list li:hover {
	-webkit-box-shadow: 0 2px 16px 2px rgba(0,0,0,.1);
	-moz-box-shadow: 0 2px 16px 2px rgba(0,0,0,.1);
	box-shadow: 0 2px 16px 2px rgba(0,0,0,.1)
}

.myOrder-list li:hover .myOrder-number a,.myOrder-list li:hover i.imv2-delete {
	display: block
}

.del-box {
	margin-left: 16px;
	width: 510px
}

.del-box .course-name {
	word-break: break-word;
	color: #07111b;
	font-size: 16px;
	margin-bottom: 8px;
	line-height: 22px
}

.del-box .price-btn-box {
	font-size: 14px;
	line-height: 14px
}

.del-box .price-btn-box .truepay-text {
	color: #93999f;
	margin-right: 5px
}

.del-box .price-btn-box .course-little-price {
	color: #f01414
}

.myOrder-number {
	padding: 28px 0 19px;
	font-weight: 700;
	color: #4d555d;
	border-bottom: 1px solid #b7bbbf;
	font-size: 14px;
	line-height: 14px;
	box-sizing: border-box
}

.myOrder-number a,.myOrder-number span {
	color: #93999f;
	font-weight: 500;
	margin-left: 24px
}

.myOrder-number a {
	display: none
}

.myOrder-number a:hover {
	color: #4d555d
}

.myOrder-number i.imv2-delete,.myOrder-number i.imv2-receipt {
	float: left;
	margin-top: -2px;
	margin-right: 10px;
	font-size: 16px;
	color: #f01414
}

.myOrder-number i.imv2-delete {
	float: right;
	margin-left: 28px;
	color: #93999f;
	cursor: pointer;
	display: none
}

.myOrder-number i.imv2-delete:hover {
	color: #4d555d
}

.myOrder-course {
	position: relative;
	margin-top: 25px
}

.course-money {
	width: 250px;
	height: 100%;
	text-align: center;
	color: #93999f;
	font-size: 16px;
	box-sizing: border-box;
	line-height: 16px
}

.course-money .wrap {
	display: inline-block
}

.course-money .RMB {
	font-size: 14px;
	vertical-align: top;
	line-height: 14px
}

.course-money .type-box {
	line-height: 14px;
	text-align: left
}

.course-money .type-box .type-price,.course-money .type-box .type-text {
	font-size: 16px;
	color: #93999f
}

.course-money .type-box .type-price .RMB,.course-money .type-box .type-text .RMB {
	font-size: 14px;
	display: inline-block;
	position: relative;
	top: -1px;
	vertical-align: top;
	line-height: 14px
}

.course-money .type-box .line-though {
	text-decoration: line-through
}

.course-money .type-box .type-text {
	margin-right: 5px
}

.course-money .total-box .type-text {
	font-size: 14px;
	color: #93999f;
	margin-right: 5px
}

.course-money .total-box .type-price {
	color: #f01414
}

.course-money .mb10 {
	margin-bottom: 10px
}

.course-money.presale .type-box {
	line-height: 18px;
	margin-bottom: 4px
}

.course-money.presale .type-box .type-text {
	color: #1c1f21
}

.course-money.presale .type-box .type-price .RMB {
	vertical-align: baseline
}

.course-action {
	position: absolute;
	top: 0;
	width: 180px;
	height: 100%;
	border-left: 1px solid #d9dde1;
	right: 0;
	text-align: center
}

.course-action .pay-now {
	margin: 12px auto;
	display: block;
	width: 120px;
	height: 36px;
	color: #fff;
	background: rgba(240,20,20,.8);
	border-radius: 18px;
	line-height: 36px
}

.course-action .pay-now:hover {
	background-color: #f01414
}

.course-action .order-cancel {
	color: #93999f;
	display: block;
	font-size: 14px;
	line-height: 14px
}

.course-action .order-cancel:hover {
	color: #4d555d
}

.course-action .order-close {
	color: #93999f;
	margin-top: 36px;
	line-height: 14px
}

.course-action.order-recover .order-close {
	margin-top: 22px
}

.course-del {
	width: 740px;
	border-right: 1px solid #d9dde1;
	position: relative
}

</style>