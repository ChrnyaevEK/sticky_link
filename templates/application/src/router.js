import Vue from "vue";
import VueRouter from "vue-router";
import AppEdit from "./components/App/AppEdit";
import AppView from "./components/App/AppView";
import AppEmpty from "./components/App/AppEmpty";
import WallEdit from "./components/Wall/WallEdit";
import WallView from "./components/Wall/WallView";
import WallEmpty from "./components/Wall/WallEmpty";
import WallForbidden from "./components/Wall/WallForbidden";
import store from "./store";

Vue.use(VueRouter);

var router = new VueRouter({
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
                        if (store.dispatch("validateWall", { id: to.params.wallId })) {
                            store.dispatch("fetchWidgets", to.params.wallId).then(next);
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
                        if (store.dispatch("validateWall", { id: to.params.wallId })) {
                            store.dispatch("fetchWidgets", to.params.wallId).then(next);
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
                    name: "appEmpty",
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
    Promise.all([store.dispatch("fetchUser"), store.dispatch("fetchSettings"), store.dispatch("fetchWalls")]).then(next);
});

export default router;
