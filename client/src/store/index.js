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
export default new Vuex.Store({
  state: {
    isAuth: JSON.parse(localStorage.getItem('isAuth')),
    userInfo: JSON.parse(localStorage.getItem('userInfo')), // new User()
    orders:JSON.parse(localStorage.getItem('orders')),
    requests:JSON.parse(localStorage.getItem('requests'))
  },
  getters: {
    // 转换为bool值
    isAuth: state => state.isAuth
  },
  mutations: {
    //save the login state
    userStatus(state, setState) {
      state.isAuth = setState
      localStorage.setItem('isAuth', JSON.stringify(setState))
    },
    saveUserInfo(state, userlikeObj) {
      state.userInfo = new User(userlikeObj);
      localStorage.setItem('userInfo', JSON.stringify(state.userInfo))
    },
    deleteUserInfo(state) {
      state.userInfo = null
      localStorage.removeItem('userInfo')
    },
    saveOrders(state,orderList){
      state.orders = orderList
      localStorage.setItem('orders', JSON.stringify(state.orders))
    },
    saveRequests(state,requestList){
      state.requests = requestList
      localStorage.setItem('requests', JSON.stringify(state.requests))
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