import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Error from "../components/Error";
import Wall from "../components/Wall";
import store from "./store";
import env from "./env";
import $ from "jquery";

Vue.use(VueRouter);
const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/",
            component: App,
            name: "home",
            redirect: { name: "wallEdit" },
            children: [
                {
                    name: "wallEdit",
                    path: "edit/wall/:wallId?",
                    component: Wall,
                    async beforeEnter(to, from, next) {
                        if (!store.state.user.is_authenticated) {
                            return next({
                                name: "home",
                            });
                        }
                        if (store.state.meta && !store.state.meta.edit_permission) {
                            return next({
                                name: "home",
                            });
                        }

                        await env.dispatch("setEditMode");
                        next();
                    },
                },
                {
                    name: "wallView",
                    path: "view/wall/:wallId",
                    component: Wall,
                    async beforeEnter(to, from, next) {
                        if (!store.state.meta.view_permission) {
                            return next({
                                name: "home",
                            });
                        }
                        await env.dispatch("setViewMode");
                        next();
                    },
                },
                {
                    name: "error",
                    path: "/error",
                    component: Error,
                },
                {
                    path: "*",
                    redirect: { name: "home" },
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
    if (to.name != "error") {
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
