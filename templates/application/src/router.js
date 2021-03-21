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

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/app/edit",
            component: AppEdit,
            children: [
                {
                    name: "wallEdit",
                    path: "wall/:wallId",
                    component: WallEdit,
                    beforeEnter(to, from, next) {
                        if (store.state.user.is_anonymous) {
                            next({
                                name: "wallView",
                                params: {
                                    wallId: to.params.wallId,
                                },
                            });
                        } else {
                            store.dispatch("fetchWalls").then(() => {
                                store.dispatch("validateWall", { id: to.params.wallId }).then((ok) => {
                                    if (ok) {
                                        store.dispatch("fetchWidgets", to.params.wallId).then(next);
                                    } else {
                                        next({
                                            name: "wallForbidden",
                                        });
                                    }
                                });
                            });
                        }
                    },
                },
            ],
        },
        {
            path: "/app/view",
            component: AppView,
            children: [
                {
                    name: "wallView",
                    path: "wall/:wallId",
                    component: WallView,
                    beforeEnter(to, from, next) {
                        store.dispatch("fetchWalls").then(() => {
                            store.dispatch("validateWall", { id: to.params.wallId }).then((ok) => {
                                if (ok) {
                                    store.dispatch("fetchWidgets", to.params.wallId).then(next);
                                } else {
                                    next({
                                        name: "wallForbidden",
                                    });
                                }
                            });
                        });
                    },
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
                    component: WallEmpty,
                    beforeEnter(to, from, next) {
                        if (store.state.user.is_authenticated) {
                            store.dispatch("fetchWalls").then(next);
                        } else {
                            next();
                        }
                    },
                },
            ],
        },
        {
            path: "/app",
            component: AppEmpty,
            beforeEnter(to, from, next) {
                if (store.state.user.is_authenticated) {
                    store.dispatch("fetchWalls").then(next);
                } else {
                    next();
                }
            },
            children: [
                {
                    name: "wallForbidden",
                    path: "",
                    component: WallForbidden,
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
    Promise.all([store.dispatch("fetchUser"), store.dispatch("fetchSettings")]).then(next);
});

export default router;
