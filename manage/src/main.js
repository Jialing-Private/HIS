import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import 'font-awesome/css/font-awesome.min.css';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import "./assets/style.css";

Vue.use(ElementUI);
Vue.config.productionTip = false;

import initMenu from "./utils/menus.js";

router.beforeEach((to,from,next)=>{

  if(to.path == '/'){
    next();
  }else{
    if(store.state.menus != null && store.state.menus.length > 0){

      next();
    }else{

      initMenu(router, store);
      next();
    }
  }
});

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
