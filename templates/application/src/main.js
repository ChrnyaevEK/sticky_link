import Vue from 'vue'
import 'bootstrap'
import App from './App.vue'
import './static/main.scss';
import '@fortawesome/fontawesome-free/js/all.js';
import '@fortawesome/fontawesome-free/css/all.css';
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
