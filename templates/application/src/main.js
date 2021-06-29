import Vue from "vue";
import router from "./modules/router";
import env from "./modules/env";
import proxy from "./modules/proxy";
import store from "./modules/store";
import io from "./modules/io";
import "bootstrap";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
import $ from "jquery";
import Notifications from "vue-notification";

Vue.use(Notifications);

Vue.config.productionTip = false;
Vue.prototype.$env = env;
Vue.prototype.$proxy = proxy;
Vue.prototype.$io = io;
Vue.prototype._ = function (value) {
    return this._uid + "-" + value;
};
Vue.directive("scope", {
    // v-scope:<id>.<property> => id="xxx-property"
    bind: (el, binding, vnode) => {
        let value = Object.keys(binding.modifiers).join("") || binding.value;
        el.setAttribute(binding.arg, vnode.context._(value));
    },
});

window.jQuery = $; // Ref. to rollbar-jquery source code

if (process.env.NODE_ENV === "production") {
    window.gtag("js", new Date());
    window.gtag("config", "G-NGS03ZXLXN");
}
new Vue({
    router,
    store,
    template: "<router-view/>",
}).$mount("#app");
