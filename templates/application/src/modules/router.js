import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Error from "../components/Error";
import store from "./store";
import env from "./env";
import $ from "jquery";

import WallEditor from "../components/Wall/Editor";
import WallOverview from "../components/Wall/Overview";
import WallSettings from "../components/Wall/Settings";

import PortSettings from "../components/Port/Settings";
import PortOverview from "../components/Port/Overview";


Vue.use(VueRouter);
const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/",
            component: App,
            name: "home",
            redirect: {name: "wallOverview"},
            children: [

                {
                    name: "wallEdit",
                    path: "wall/edit/:wallId?",
                    component: WallEditor,
                    async beforeEnter(to, from, next) {
                        if (to.params.wallId !== undefined) {
                            if (
                                store.state.meta &&
                                !store.state.meta.edit_permission &&
                                store.state.meta.view_permission
                            ) {
                                return next({
                                    name: "wallView",
                                    params: {
                                        wallId: to.params.wallId,
                                    },
                                });
                            }
                        } else {
                            if (!store.state.user.is_authenticated) {
                                location.href = process.env.VUE_APP_LOGIN;
                                return;
                            }
                        }

                        await env.dispatch("setEditMode");
                        next();
                    },
                },
                {
                    name: "wallView",
                    path: "wall/view/:wallId",
                    component: WallEditor,
                    async beforeEnter(to, from, next) {
                        if (store.state.meta) {
                            if (!store.state.meta.view_permission) {
                                return next({
                                    name: "home",
                                });
                            }
                        } else {
                            return next({
                                name: "home",
                            });
                        }
                        await env.dispatch("setViewMode");
                        next();
                    },
                },
                {
                    name: "wallSettings",
                    path: "wall/settings/:wallId",
                    component: WallSettings,
                },
                {
                    name: 'wallOverview',
                    path: 'wall/overview',
                    component: WallOverview,
                },
                {
                    name: 'portSettings',
                    path: 'port/settings/:portId',
                    component: PortSettings,
                },
                {
                    name: 'portOverview',
                    path: 'port/overview',
                    component: PortOverview,
                },
                {
                    name: "error",
                    path: "/error",
                    component: Error,
                },
                {
                    path: "*",
                    redirect: {name: "home"},
                },
            ],
        },
        {
            path: "*",
            redirect: "/",
        },
    ],
});
router.beforeEach(async (to, from, next) => {
    if (to.name !== "error") {
        try {
            await store.dispatch("fetchState", to.params.wallId);
        } catch (e) {
            return next({
                name: "error",
            });
        }
    }
    if (store.state.user) {
        $("#tab-title").text(`${store.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
    }
    next();
});
export default router;
