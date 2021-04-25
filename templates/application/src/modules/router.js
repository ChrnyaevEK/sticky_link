import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Wall from "../components/Wall";
import store from "./store";
import env from "./env";
import ws from "./ws";

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
                    beforeEnter(to, from, next) {
                        if (env.wall && !store.state.meta.edit_permission) {
                            return next({ to: "wallView", params: to.params });
                        }
                        if (to.params.wallId !== undefined) {
                            ws.open(to.params.wallId);
                        }
                        env.edit = true;
                        next();
                    },
                },
                {
                    name: "wallView",
                    path: "wall/view/:wallId?",
                    component: Wall,
                    beforeEnter(to, from, next) {
                        if (env.wall && !store.state.meta.view_permission) {
                            return next({ to: "wallEdit" });
                        }
                        if (to.params.wallId !== undefined) {
                            ws.open(to.params.wallId);
                        }
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
    await env.closeOptions()
    env.wallId = to.params.wallId;
    env.setTabTitle();
    if (store.state.containers) {
        let container = store.state.containers[0];
        env.containerId = container ? container.id : null;
    }
    Vue.nextTick(next);
});

export default router;
