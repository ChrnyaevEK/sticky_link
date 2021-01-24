import Vue from 'vue'
import 'bootstrap'
import App from './App.vue'
import './static/main.scss';

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
