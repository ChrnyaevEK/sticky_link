import Vue from "vue";
import router from "./router";
import "bootstrap";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
import { env, ws, generateId, handleUnexpected } from "./common";
import store from "./store";
import $ from "jquery";
import Rollbar from "rollbar";
import JqueryRollbarPlugin from "rollbar-jquery";

Vue.config.productionTip = true;
Vue.prototype.$env = env;
Vue.prototype._ = generateId;

window.jQuery = $; // Ref. to rollbar-jquery source code
JqueryRollbarPlugin();

export var rollbar = new Rollbar({
    accessToken: "352f084b3c4b4a60951b25ce2252fb6f",
    captureUncaught: process.env.NODE_ENV == "production",
    captureUnhandledRejections: process.env.NODE_ENV == "production",
    payload: {
        environment: "production",
    },
});
rollbar.global({ itemsPerMinute: 5 });
rollbar.configure({ reportLevel: "error" });
rollbar.configure({
    onSendCallback: function(isUncaught) {
        if (isUncaught) {
            handleUnexpected();
        }
    },
});

new Vue({
    router,
    store,
    template: "<router-view/>",
    watch: {
        $route: {
            handler: function(to, from) {
                // Reconnect to server on route change (on wall change)
                if (to.params.wallId !== undefined) {
                    if (to.params.wallId !== from.params.wallId) {
                        ws.connect(to.params.wallId);
                    }
                }
            },
            deep: true,
        },
    },
}).$mount("#app");
