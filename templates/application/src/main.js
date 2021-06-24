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
import Rollbar from 'vue-rollbar'
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

Vue.use(Rollbar, {
    enabled: process.env.NODE_ENV === "production",
    accessToken: "352f084b3c4b4a60951b25ce2252fb6f",
    captureUncaught: process.env.NODE_ENV === "production",
    captureUnhandledRejections: process.env.NODE_ENV === "production",
    payload: {
        environment: "production",
    },
});

if (process.env.NODE_ENV === "production") {
    window.gtag("js", new Date());
    window.gtag("config", "G-NGS03ZXLXN");
}
new Vue({
    router,
    store,
    template: "<router-view/>",
}).$mount("#app");
