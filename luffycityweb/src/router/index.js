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
    meta:{
        title: "luffy2.0-个人中心",
        keepAlive: true,
    },
    path: '/user',
    name: "User",
    component: ()=> import("../views/User.vue"),
    },
    {
    meta:{
        title: "luffy2.0-课程列表",
        keepAlive: true,
    },
    path: '/project',
    name: "Course",
    component: ()=> import("../views/Course.vue"),
  },
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