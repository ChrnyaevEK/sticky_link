import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Wall from "../components/Wall";
import store from "./store";
import env from "./env";

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
                    alias: '',
                    component: Wall,
                    beforeEnter(to, from, next) {
                        env.edit = true;
                        next();
                    },
                },
                {
                    name: "wallView",
                    path: "wall/view/:wallId?",
                    component: Wall,
                    beforeEnter(to, from, next) {
                        env.edit = false;
                        next();
                    },
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
    await store.dispatch("fetchState", to.params.wallId);
    next();
});

export default router;
