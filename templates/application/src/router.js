import Vue from "vue";
import VueRouter from "vue-router";
import App from "./components/App";
import Wall from "./components/Wall";
import store from "./store";
import { env } from "./common";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/app",
            component: App,
            children: [
                {
                    name: "wall",
                    path: "wall/:wallId?",
                    alias: ":wallId?",
                    component: Wall,
                    beforeEnter(to, from, next) {
                        if (to.query.edit) {
                            env.openEditor()
                        } else {
                            env.closeEditor()
                        }
                        next()
                    },
                },
            ],
        },
        {
            path: "*",
            redirect: "/app",
        },
        {
            path: "/",
            name: "home",
            beforeEnter() {
                window.location.replace(location.origin);
            },
        },
        {
            path: "/accounts/login/",
            name: "login",
            beforeEnter(to) {
                window.location.replace(location.origin + to.path);
            },
        },
        {
            path: "/accounts/logout/",
            name: "logout",
            beforeEnter(to) {
                window.location.replace(location.origin + to.path);
            },
        },
    ],
});

router.beforeEach(async (to, from, next) => {
    await store.dispatch("fetchState", to.params.wallId);
    next();
});

export default router;
