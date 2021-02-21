import Vue from "vue";
import VueRouter from "vue-router";
import "bootstrap";
import App from "./App.vue";
import Wall from "./components/Wall";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
Vue.config.productionTip = true;
Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/app/",
            name: "app",
            component: App,
            children: [
                {
                    name: "wall",
                    path: "wall/:wallId",
                    component: Wall,
                },
            ],
        },
    ],
});

new Vue({
    router,
    template: "<router-view/>",
}).$mount("#app");
