import Vue from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
// import axios from "./axios";
// import mock from './mock';
import vuetify from "./plugins/vuetify";
// import ElementUI from 'element-ui';
// import 'element-ui/lib/theme-chalk/index.css';

// import Vuetify from "@/plugins/vuetify";
// import "vuetify/dist/vuetify.min.css";
// import "vuetify/";

import axios from "axios";
import VueAxios from "vue-axios";
import VueCsrf from "vue-csrf";

Vue.config.productionTip = false;

// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
// axios.defaults.headers.common['Content-Type'] = 'application/x-www-form-urlencoded';
// axios.defaults.headers.common['X-CSRF-TOKEN'] = document.querySelector('#token').getAttribute('value');
// axios.defaults.xsrfCookieName = 'csrftoken'
// axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

// axios.interceptors.request.use(config => {
//   const cookies = window.cookies
//   if (cookies && config.method === 'post') {
//     config.headers['x-csrftoken'] = cookies.get('csrftoken');
//   }
//   return config
// })

// Vue.use(ElementUI);
Vue.use(vuetify);
Vue.use(store);
Vue.use(router);
Vue.use(VueAxios, axios);
Vue.use(VueCsrf);

// 登录拦截
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (store.getters.isAuth) {
      next();
      return;
    }
    alert("请先登录");
    next({
      name: "Login",
    });
  } else {
    if (
      store.getters.isAuth &&
      (to.name === "Login" || to.name === "Register")
    ) {
      alert("请先退出登录");
      next(from);
      return;
    }
    else if(to.meta.requireAdminAuth){
      if(store.getters.isAdminAuth){
        next()
      }
      alert("管理员请先登录");
      next()
    }
    next();
  }

  // 检测路由配置中是否有requiresAuth这个meta属性
  // if (to.matched.some(record => record.meta.requireAuth)) {
  //   // 判断是否已登录
  //   if (store.getters.isAuth) {
  //     next();
  //     return;
  //   }
  //   // 未登录则跳转到登录界面
  //   alert("请先登录")
  //   next({
  //     name: 'Login'
  //   });
  // } else {
  //   next()
  // }
});

router.afterEach(() => {
  window.scroll(0, 0);
});

new Vue({
  store,
  router,
  vuetify,
  // mock,
  render: (h) => h(App),
}).$mount("#app");
