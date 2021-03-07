import Vue from "vue";
import router from "./router";
import "bootstrap";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
import {env, generateId} from "./common";
import store from "./store";

Vue.config.productionTip = true;
Vue.prototype.$env = env;
Vue.prototype._ = generateId;
new Vue({
    router,
    store,
    template: "<router-view/>",
}).$mount("#app");
