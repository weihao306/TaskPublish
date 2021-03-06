import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "../store";
// import {
//   component
// } from 'vue/types/umd'

Vue.use(VueRouter);

const mainViews = [{
    path: 'SummoningOrder',
    name: 'SummoningOrderMain',
    component: () => import('../views/SummoningOrder/Main.vue'),
    meta: {
      requireAuth: true
    }
  },
  {
    path: 'SummoningOrder/Master',
    name: 'Master',
    component: () => import('../views/SummoningOrder/Master.vue'),
    meta: {
      requireAuth: true
    }
  },
  {
    path: 'SummoningOrder/Master/OrderInfo/:order_id',
    name: 'OrderInfo',
    component: () => import('../views/SummoningOrder/OrderInfo.vue'),
    props: true,
    // parmas:{
    //   order_id:Number
    // },
    meta: {
      requireAuth: true
    }

  },
  {
    path: 'SummoningOrder/Master/PublishOrder',
    name: 'PublishOrder',
    component: () => import('../views/SummoningOrder/PublishOrder.vue'),
    meta: {
      requireAuth: true
    }
  },
  {
    path: 'SummoningOrder/Masses',
    name: 'Masses',
    component: () => import('../views/SummoningOrder/Masses.vue'),
    meta: {
      requireAuth: true
    }
  },
  {
    path: 'SummoningOrder/Masses/SeekOrder',
    name: 'SeekOrder',
    component: () => import("../views/SummoningOrder/SeekOrder.vue"),
    props:true,
    meta: {
      requireAuth: true
    }
  },
  {
    path: 'User',
    name: 'UserInfo',
    component: () => import('../views/User/Info.vue'),
    props:true,
    meta: {
      requireAuth: true
    }
  }
];

const routes = [{
    path: '/',
    redirect: {
      name: 'UserInfo',
      params:{
        uid:store.state.userInfo.uid
      }
    },
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: {
      requireAuth: true
    },
    children: mainViews
  },
  {
    path: '/About',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import( /* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
  },
  {
    path: '/Register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/Admin/Login',
    name: 'AdminLogin',
    component: () => import('@/views/Admin/Login.vue'),
  },
  {
    path: '/Admin/Statistics',
    name: 'Statistics',
    component: () => import('@/views/Admin/Statistics.vue'),
  },
  {
    path: '*',
    redirect: {
      name: 'UserInfo',
      params: {
        uid: store.state.userInfo.uid
      }
    }
  },
]

const router = new VueRouter({
  routes
})

// router.beforeEach(to,f)

export default router