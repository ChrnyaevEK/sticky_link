import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Error from "../components/Error";
import Wall from "../components/Wall";
import store from "./store";
import env from "./env";
import ws from "./ws";
import $ from "jquery";

Vue.use(VueRouter);
const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/",
            component: App,
            children: [
                {
                    name: "wallEdit",
                    path: "wall/edit/:wallId?",
                    alias: "",
                    component: Wall,
                    async beforeEnter(to, from, next) {
                        if (env.state.wall && !store.state.meta.edit_permission) {
                            return next({ to: "wallView", params: to.params });
                        }
                        if (to.params.wallId !== undefined) {
                            ws.open(to.params.wallId);
                        }
                        await env.dispatch("setEditMode");
                        next();
                    },
                },
                {
                    name: "wallView",
                    path: "wall/view/:wallId?",
                    component: Wall,
                    async beforeEnter(to, from, next) {
                        if (env.state.wall && !store.state.meta.view_permission) {
                            return next({ to: "wallEdit" });
                        }
                        if (to.params.wallId !== undefined) {
                            ws.open(to.params.wallId);
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
            ],
        },
        {
            path: "*",
            redirect: "/",
        },
    ],
});
router.beforeEach(async (to, from, next) => {
    try {
        await store.dispatch("fetchState", to.params.wallId);
    } catch (e) {
        return next({
            name: "error",
        });
    }
    if (store.state.user) {
        $("#tab-title").text(`${store.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
    }
    next();
});
export default router;
