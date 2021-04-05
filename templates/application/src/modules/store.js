import Vuex from "vuex";
import Vue from "vue";
import { difference } from "../common";
import env from "./env";
import api from "./api";
import um from "./um";
import io from "./io";

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
        user: null,
        walls: null,
        containers: null,
        widgets: null,
        meta: null,

        app: {
            title: process.env.VUE_APP_TITLE,
            grid: 3,
        },
    },
    mutations: {
        setState(state, response) {
            Object.assign(state, response);
        },
        deleteInstance(state, instance) {
            let source = determineSource(instance);
            for (let i = 0; i < state[source].length; i++) {
                if (state[source][i].uid == instance.uid) {
                    return state[source].splice(i, 1);
                }
            }
        },
        updateOrAddInstance(state, instance) {
            let source = determineSource(instance);
            for (let local of state[source]) {
                if (local.uid == instance.uid) {
                    return Object.assign(local, instance);
                }
            }
            state[source].push(instance);
        },
    },
    actions: {
        async fetchState(context, wallId) {
            let state = wallId != undefined ? await api.retrieve("state", wallId) : await api.get("state");
            context.commit("setState", state);
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
            io.save(true);
            let local = (await context.dispatch("getInstanceByUid", instance.uid)) || {};
            let update = difference(local, instance);
            if (Object.keys(update).length) {
                context.commit("updateOrAddInstance", instance);
                instance = await um.proposeUpdate(update, instance);
            }
            io.save(false);
            return instance;
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
            let update = [];
            for (let widget of context.state.widgets) {
                if (widget.container == container.id) {
                    widget = env.makeMutable(widget);
                    if (widget.y + widget.h >= container.h) {
                        let y = container.h - widget.h;
                        widget.y = y < 0 ? 0 : y;
                    }
                    if (widget.h >= container.h) {
                        widget.h = container.h;
                    }
                    update.push(context.dispatch("updateOrAddInstance", widget));
                }
            }
            await Promise.all(update);
        },
        getInstanceByUid(context, uid) {
            return [
                ...(context.state.walls ? context.state.walls : []),
                ...(context.state.widgets ? context.state.widgets : []),
            ].filter((instance) => instance.uid == uid)[0];
        },
    },
});
