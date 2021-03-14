import Vue from "vue";
import router from "./router";
import "bootstrap";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
import { env, ws, generateId, handleUnexpected } from "./common";
import store from "./store";

Vue.config.productionTip = true;
Vue.prototype.$env = env;
Vue.prototype._ = generateId;

window.onerror = function() {
    handleUnexpected();
};



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
