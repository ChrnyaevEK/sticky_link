import Vue from "vue";
import VueRouter from "vue-router";
import "bootstrap";
import AppEdit from "./components/App/AppEdit";
import AppView from "./components/App/AppView";
import AppEmpty from "./components/App/AppEmpty";
import WallEdit from "./components/Wall/WallEdit";
import WallView from "./components/Wall/WallView";
import WallEmpty from "./components/Wall/WallEmpty";
import WallForbidden from "./components/Wall/WallForbidden";
import "./css/main.scss";
import "@fortawesome/fontawesome-free/js/all.js";
import "@fortawesome/fontawesome-free/css/all.css";
import { Context, validateWall } from "./common.js";
Vue.config.productionTip = true;
Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/app/edit",
            component: AppEdit,
            children: [
                {
                    path: "wall",
                    redirect: "/app",
                },
                {
                    name: "wallEdit",
                    path: "wall/:wallId",
                    component: WallEdit,
                    beforeEnter(to, from, next) {
                        if (validateWall(to.params.wallId)) {
                            next();
                        } else {
                            next({
                                name: "wallEditForbidden",
                                params: {
                                    wallId: to.params.wallId,
                                },
                            });
                        }
                    },
                },
                {
                    name: "wallEditForbidden",
                    path: "wall/:wallId",
                    component: WallForbidden,
                },
            ],
        },
        {
            path: "/app/view",
            component: AppView,
            children: [
                {
                    path: "wall",
                    redirect: "/app",
                },
                {
                    name: "wallView",
                    path: "wall/:wallId",
                    component: WallView,
                    beforeEnter(to, from, next) {
                        if (validateWall(to.params.wallId)) {
                            next();
                        } else {
                            next({
                                name: "wallViewForbidden",
                                params: {
                                    wallId: to.params.wallId,
                                },
                            });
                        }
                    },
                },
                {
                    name: "wallViewForbidden",
                    path: "wall/:wallId",
                    component: WallForbidden,
                },
            ],
        },
        {
            path: "/app",
            component: AppEmpty,
            children: [
                {
                    path: "",
                    alias: "*",
                    component: WallEmpty,
                },
            ],
        },
        {
            path: "*",
            redirect: "/app",
        },
    ],
});

router.beforeEach((to, from, next) => {
    Context.initUser().then(next);
});

new Vue({
    router,
    template: "<router-view/>",
}).$mount("#app");
