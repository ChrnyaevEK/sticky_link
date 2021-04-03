import Vuex from "vuex";
import Vue from "vue";
import { difference } from "../common";
import env from "./env";
import api from "./api";
import um from "./um";

Vue.use(Vuex);

function determineSource(instance) {
    switch (instance.type) {
        case "wall":
            return "walls";
        case "container":
            return "containers";
        default:
            return "widgets";
    }
}

export default new Vuex.Store({
    strict: true,
    state: {
        valid: false,
        user: null,
        wall: null,
        walls: null,
        containers: null,
        container: null,
        widgets: null,
        app: {
            title: process.env.VUE_APP_TITLE,
        },
    },
    mutations: {
        setState(state, response) {
            state.user = response.user;
            state.wall = response.wall;
            state.walls = response.walls;
            state.containers = response.containers;
            state.container = response.container;
            state.widgets = response.widgets;
            if (state.user.is_anonymous) {
                state.user.username = "anonymous";
            }
        },
        deleteInstance(state, instance) {
            var source = determineSource(instance);
            for (var i = 0; i < state[source].length; i++) {
                if (state[source][i].uid == instance.uid) {
                    state[source].splice(i, 1);
                    break;
                }
            }
        },
        updateOrAddInstance(state, instance) {
            var source = determineSource(instance);
            for (let localInstance of state[source]) {
                if (localInstance.uid == instance.uid) {
                    return Object.assign(localInstance, instance);
                }
            }
            state[source].push(instance);
        },
        setContainer(state, container) {
            state.container = container;
        },
    },
    actions: {
        async fetchState(context, wallId) {
            if (wallId !== undefined) {
                context.commit("setState", await api.retrieve("state", wallId));
            } else {
                context.commit("setState", await api.get("state"));
            }
        },
        async fetchInstance(context, instance) {
            instance = await api.retrieve(instance.type, instance.id);
            context.commit("updateOrAddInstance", instance);
            return instance;
        },
        async createInstance(context, instance) {
            await env.lockChanges();
            instance = await api.create(instance.type, instance);
            context.commit("updateOrAddInstance", instance);
            await env.unlockChanges();
            return instance;
        },
        async deleteInstance(context, instance) {
            await env.lockChanges();
            await api.delete(instance.type, instance.id, instance.uid);
            context.commit("deleteInstance", instance);
            await env.unlockChanges();
        },
        async updateOrAddInstance(context, instance) {
            var localInstance = await context.dispatch("getInstanceByUid", instance.uid);
            var update = instance;
            if (localInstance) {
                update = difference(localInstance, instance);
            }
            if (Object.keys(update).length) {
                context.commit("updateOrAddInstance", instance);
                return await um.proposeUpdate(update, instance);
            }
        },
        async copyWidget(context, widget) {
            widget = await api.create(widget.type, {
                ...widget,
                id: undefined,
            });
            context.commit("updateOrAddInstance", widget);
            return widget;
        },
        async recalculateWidgets(context, container) {
            var updateArray = [];
            for (var widget of context.state.widgets) {
                widget = Object.assign({}, widget);
                if (widget.y + widget.h >= container.h) {
                    var y = container.h - widget.h;
                    widget.y = y < 0 ? 0 : y;
                }
                if (widget.h >= container.h) {
                    widget.h = container.h;
                }
                updateArray.push(context.dispatch("updateOrAddInstance", widget));
            }
            await Promise.all(updateArray);
        },
        getInstanceByUid(context, uid) {
            return [...context.state.walls, ...context.state.widgets].filter((i) => i.uid == uid)[0];
        },
    },
});
