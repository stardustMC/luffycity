import {createRouter, createWebHistory} from "vue-router";
import store from "../store"

const routes = [
    {
        meta:{
            title: "Luffycity Home Page",
            keepalive: true,
        },
        path: '/',
        name: 'home',
        component: ()=> import("../views/Home.vue")
    },
    {
        meta:{
            title: "Luffycity Login Page",
            keepalive: true,
        },
        path: '/login',
        name: 'login',
        component: ()=> import("../views/Login.vue")
    },
    {
        meta: {
            title: "luffy2.0-个人中心",
            keepAlive: true,
        },
        path: '/user',
        name: "User",
        component: () => import("../views/User.vue"),
        children:[
            {
                meta: {
                    title: "个人订单",
                    keepAlive: true,
                    authorization: true,
                },
                path: 'order',
                name: "UserOrder",
                component: () => import("../components/user/Order.vue")
            },
            {
                meta: {
                    title: "个人信息",
                    keepAlive: true,
                    authorization: true,
                },
                path: '',
                name: "UserInfo",
                component: () => import("../components/user/Info.vue")
            },
            {
                meta: {
                    title: "个人课程",
                    keepAlive: true,
                    authorization: true,
                },
                path: 'course',
                name: "UserCourse",
                component: () => import("../components/user/Course.vue")
            }
        ]
    },
    {
        meta: {
            title: "luffy2.0-课程列表",
            keepAlive: true,
        },
        path: '/project',
        name: "Course",
        component: () => import("../views/Course.vue"),
    },
    {
        meta: {
            title: "luffy2.0-课程详情",
            keepAlive: true,
        },
        path: "/project/:id",
        name: "CourseInfo",
        component: ()=>import("../views/Info.vue"),
    },
    {
        meta: {
            title: "luffy2.0-购物车列表",
            keepAlive: true,
        },
        path: "/cart",
        name: "Cart",
        component: ()=>import("../views/Cart.vue"),
    },
    {
        meta: {
            title: "luffy2.0-OrderPay",
            keepAlive: true,
        },
        path: "/order",
        name: "Order",
        component: ()=>import("../views/Order.vue"),
    },
    {
        meta: {
            title: "luffy2.0-订单详情"
        },
        path: "/feedback",
        name: "Feedback",
        component: ()=>import("../views/AlipaySuccess.vue"),
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 导航守卫
router.beforeEach((to, from, next)=>{
  document.title=to.meta.title
  // 登录状态验证
  if (to.meta.authorization && !store.getters.getUserInfo) {
    next({"name": "Login"})
  }else{
    next()
  }
})

export default router;