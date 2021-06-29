import Vue from "vue";
import VueRouter from "vue-router";
import App from "../components/App";
import Error from "../components/Error";
import Profile from "../components/Profile";
import store from "./store";
import env from "./env";
import $ from "jquery";

import WallEditor from "../components/Wall/Editor";
import WallOverview from "../components/Wall/Overview";
import WallSettings from "../components/Wall/Settings";

import PortSettings from "../components/Port/Settings";
import PortOverview from "../components/Port/Overview";
import NotAuthenticated from "../components/NotAuthenticated";


function checkExist(source, id) {
    for (let i of source) {
        if (i.id === id) {
            return true
        }
    }
    return false
}

async function guardOwned(to, from, next, key, route, source) {
    if (!checkExist(source, to.params[key]) || (store.state.reference && !store.state.reference.owner_permission)) {
        return next({
            name: route,
            params: to.params,
        });
    }
    await env.dispatch("setEditMode");
    next();
}

async function guardTrusted(to, from, next, key, route, source) {
    if (
        !checkExist(source, to.params[key]) ||
        (store.state.reference && !store.state.reference.owner_permission && !store.state.reference.trusted_permission)
    ) {
        return next({
            name: route,
            params: to.params,
        });
    }
    await env.dispatch("setEditMode");
    next();
}

async function guardViewable(to, from, next) {
    if (
        !store.state.reference.owner_permission &&
        !store.state.reference.trusted_permission &&
        !store.state.reference.anonymous_permission
    ) {
        return next({
            name: "home",
        });
    }
    await env.dispatch("setViewMode");
    next();
}

function guardAuthenticated(to, from, next) {
    if (!store.state.user.is_authenticated) {
        return next({
            name: "notAuthenticated",
        })
    }
    return next()
}


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
                        await guardTrusted(to, from, next, 'wallId', 'wallView', store.state.walls)
                    },
                },
                {
                    name: "wallView",
                    path: "wall/view/:wallId",
                    component: WallEditor,
                    async beforeEnter(to, from, next) {
                        await guardViewable(to, from, next)
                    },
                },
                {
                    name: "wallSettings",
                    path: "wall/settings/:wallId",
                    component: WallSettings,
                    async beforeEnter(to, from, next) {
                        await guardOwned(to, from, next, 'wallId', 'home', store.state.walls)
                    },
                },
                {
                    name: 'wallOverview',
                    path: 'wall/overview',
                    component: WallOverview,
                    beforeEnter(to, from, next) {
                        guardAuthenticated(to, from, next)
                    }
                },
                {
                    name: 'portSettings',
                    path: 'port/settings/:portId',
                    component: PortSettings,
                    async beforeEnter(to, from, next) {
                        await guardOwned(to, from, next, 'portId', 'home', store.state.ports)
                    },
                },
                {
                    name: 'portOverview',
                    path: 'port/overview',
                    component: PortOverview,
                    beforeEnter(to, from, next) {
                        guardAuthenticated(to, from, next)
                    }
                },
                {
                    name: "error",
                    path: "/error",
                    component: Error,
                },
                {
                    name: "notAuthenticated",
                    path: "/continue",
                    component: NotAuthenticated,
                },
                {
                    name: "profile",
                    path: "/profile",
                    component: Profile,
                    beforeEnter(to, from, next) {
                        guardAuthenticated(to, from, next)
                    }
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
            if (e.status >= 500) {
                return next({
                    name: "error",
                });
            } else {
                return next({
                    name: "home",
                });
            }
        }
    }
    if (store.state.user) {
        $("#tab-title").text(`${store.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
    }
    next();
});
export default router;
