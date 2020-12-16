import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// class User{
//   uid;
//   nickName;
//   account;
//   password;
//   introduction;
//   cert_type;
//   cert_number;
//   constructor(uid,nickName,account,password,introduction,cert_type,cert_number) {
//     this.uid = uid;
//     this.nickName = nickName;
//     this.account = account;
//     this.password = password;
//     this.introduction = introduction;
//     this.cert_type = cert_type;
//     this.cert_number = cert_number;
//   }
// }

import User from "@/classes/User.js";
import Order from "@/classes/Order.js";
import Request from "@/classes/Request.js";
export default new Vuex.Store({
  state: {
    isAuth: JSON.parse(localStorage.getItem('isAuth')),
    isAdminAuth: JSON.parse(localStorage.getItem("isAdminAuth")),
    userInfo: new User(JSON.parse(localStorage.getItem('userInfo'))), // new User()
    orders: JSON.parse(localStorage.getItem('orders')),
    requests: JSON.parse(localStorage.getItem('requests')),
    orderStatus: {
      0: "等待召集",
      1: "召集中",
      2: "已删除",
      3: "逾期"
    },
    statusColor: {
      0: "warning",
      1: "success",
      2: "error",
      3: "default"
    },
    requestStatus: {
      0: "等待处理",
      1: "同意",
      2: "拒绝"
    },
  },
  getters: {
    // 转换为bool值
    isAuth: state => state.isAuth,
    isAdminAuth: state => state.isAdminAuth
  },
  mutations: {
    //save the login state
    userStatus(state, setState) {
      state.isAuth = setState
      localStorage.setItem('isAuth', JSON.stringify(setState))
    },
    AdminStatus(state, setState) {
      state.isAdminAuth = setState
      localStorage.setItem('isAuth', JSON.stringify(setState))
    },
    saveUserInfo(state, userlikeObj) {
      if (userlikeObj instanceof User) {
        state.userInfo = userlikeObj;
      } else {
        state.userInfo = new User(userlikeObj);
      }
      localStorage.setItem('userInfo', JSON.stringify(state.userInfo))
    },
    deleteUserInfo(state) {
      state.userInfo = null
      localStorage.removeItem('userInfo')
    },
    saveOrders(state, orderList) {
      state.orders = orderList
      localStorage.setItem('orders', JSON.stringify(state.orders))
    },
    saveRequests(state, requestList) {
      state.requests = requestList
      localStorage.setItem('requests', JSON.stringify(state.requests))
    },
    appendOrder(state, order) {
      if (order instanceof Order) {
        state.orders.push(order)
      } else {
        state.orders.push(new Order(order))
      }
    },
    appendRequest(state, request) {
      if (request instanceof Request) {
        state.requests.push(request)
      } else {
        state.requests.push(new Order(request))
      }
    }

  },
  // apply the mutations
  actions: {
    // access to the login state
    loginAction({
      commit
    }, userlikeObj) {
      commit("userStatus", true)
      commit("saveUserInfo", userlikeObj)
    },
    logoutAction({
      commit
    }) {
      commit("userStatus", false)
      commit("deleteUserInfo")
    },

  },
  modules: {}
})