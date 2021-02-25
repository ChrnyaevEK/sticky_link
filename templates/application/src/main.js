import Vue from "vue";
import VueRouter from "vue-router";
import "bootstrap";
import AppEdit from "./components/App/AppEdit";
import AppView from "./components/App/AppEdit";
import AppEmpty from "./components/App/AppEdit";
import WallEdit from "./components/Wall/WallEdit";
import WallView from "./components/Wall/WallView";
import WallEmpty from "./components/Wall/WallEmpty";
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
            children: [
                {
                    name: "appEdit",
                    path: "edit/",
                    component: AppEdit,
                    children: [
                        {
                            path: "wall/",
                            redirect: "/app/",
                        },
                        {
                            name: "wallEdit",
                            path: "wall/:wallId",
                            component: WallEdit,
                        },
                    ],
                },
                {
                    name: "appView",
                    path: "view/",
                    component: AppView,
                    children: [
                        {
                            path: "wall/",
                            redirect: "/app/",
                        },
                        {
                            name: "wallView",
                            path: "wall/:wallId",
                            component: WallView,
                        },
                    ],
                },
                {
                    path: "",
                    component: AppEmpty,
                    children: [
                        {
                            path: "",
                            component: WallEmpty,
                        },
                    ],
                },
            ],
        },
        {
            path: "*",
            component: App,
            redirect: "/app/",
        },
    ],
});

new Vue({
    router,
    template: "<router-view/>",
}).$mount("#app");
