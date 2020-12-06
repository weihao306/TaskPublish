import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
// import mock from './mock';
import vuetify from './plugins/vuetify';
// import ElementUI from 'element-ui';
// import 'element-ui/lib/theme-chalk/index.css';

// import Vuetify from "@/plugins/vuetify";
// import "vuetify/dist/vuetify.min.css";
// import "vuetify/";

import axios from "axios";
import VueAxios from "vue-axios";



Vue.config.productionTip = false;

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

// Vue.use(ElementUI);
Vue.use(vuetify);
Vue.use(router);
Vue.use(store);
Vue.use(VueAxios, axios);


// 登录拦截
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    if (store.getters.isAuth) {
      next();
      return;
    }
    alert("请先登录");
    next({
      name: 'Login'
    });
  } else {
    if (store.getters.isAuth) {
      alert("请先退出登录");
      next(from);
      return;
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
  window.scroll(0, 0)
})

new Vue({
  store,
  router,
  vuetify,
  // mock,
  render: h => h(App)
}).$mount('#app')