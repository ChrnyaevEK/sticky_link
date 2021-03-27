import Vue from "vue";
import VueRouter from "vue-router";
import App from "./components/App";
import Wall from "./components/Wall";
import store from "./store";

Vue.use(VueRouter);

const router = new VueRouter({
    mode: "history",
    routes: [
        {
            path: "/",
            name: "home",
            beforeEnter() {
                window.location.replace(location.origin);
            },
        },
        {
            path: "/app",
            component: App,
            children: [
                {
                    name: "wall",
                    path: "wall/:wallId?",
                    component: Wall,
                },
            ],
        },
        {
            path: "*",
            redirect: "/app",
        },
    ],
});

router.beforeEach(async (to, from, next) => {
    await store.dispatch("fetchState", to.params.wallId)
    next()
});

export default router;
