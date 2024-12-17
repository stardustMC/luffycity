import {createRouter, createWebHistory} from "vue-router";

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
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;