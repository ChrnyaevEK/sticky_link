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
        case "port":
            return "ports";
        default:
            return "widgets";
    }
}

function fitWidget(widget, container) {
    if (widget.x + widget.w >= container.w) {
        let x = container.w - widget.w;
        widget.x = x < 0 ? 0 : x;
    }
    if (widget.y + widget.h >= container.h) {
        let y = container.h - widget.h;
        widget.y = y < 0 ? 0 : y;
    }
    if (widget.h >= container.h) {
        widget.h = container.h;
    }
    return widget;
}

export default new Vuex.Store({
    strict: true,
    state: {
        user: null,

        walls: null,
        containers: null,
        ports: null,
        widgets: null,

        meta: null,

        app: {
            title: process.env.VUE_APP_TITLE,
            url: process.env.VUE_APP_URL,
            sourceURL: process.env.VUE_APP_API_HOST + "/source/",
            grid: 5,
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
            let state = wallId === undefined ? await api.get("state") : await api.retrieve("state", wallId);
            context.commit("setState", state);
        },
        async fetchInstance(context, instance) {
            instance = await api.retrieve(instance.type, instance.id);
            context.commit("updateOrAddInstance", instance);
            return instance;
        },
        async createInstance(context, instance) {
            await env.dispatch("lockChanges");
            instance = await api.create(instance.type, instance);
            context.commit("updateOrAddInstance", instance);
            await env.dispatch("unlockChanges");
            return instance;
        },
        async deleteInstance(context, instance) {
            await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
            await um.cancelPending(instance); // cancel or wait for pending update
            await api.delete(instance.type, instance.id, instance.uid); // Perform delete
            context.commit("deleteInstance", instance); // Delete local copy
            await env.dispatch("unlockChanges"); // Unlock changes
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
            widget = {
                ...widget,
                x: widget.x + context.state.app.grid,
                y: widget.y + context.state.app.grid,
            };
            for (let container of context.state.containers) {
                if (widget.container == container.id) {
                    widget = fitWidget(widget, container);
                    break;
                }
            }
            widget = await api.create(widget.type, widget);
            context.commit("updateOrAddInstance", widget);
            return widget;
        },

        async recalculateWidgets(context, container) {
            let update = [];
            for (let widget of context.state.widgets) {
                if (widget.container == container.id) {
                    widget = fitWidget(Object.assign({}, widget), container);
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
        async uploadSource(context, { data, name, instance }) {
            io.save(true);
            data = await api.upload(instance.source.id, name, data);
            Vue.notify({
                text: "Success!",
                type: "success",
            });
            io.save(false);
            return data;
        },
        async removeSource(context, instance) {
            io.save(true);
            await api.delete("source", instance.source.id);
            Vue.notify({
                text: "Success!",
                type: "success",
            });
            io.save(false);
        },
    },
});
