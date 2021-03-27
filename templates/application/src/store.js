import Vuex from "vuex";
import Vue from "vue";
import { env, api, updateManager, difference, deepCopy } from "./common";

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
        widgets: null,
        app: {
            title: process.env.VUE_APP_TITLE,
        },
    },
    mutations: {
        setState(state, response) {
            state.user = response.user;
            state.wall = wall;
            state.walls = walls;
            state.widgets = widgets;
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
            var localInstance = state[source].filter((i) => {
                return i.uid == instance.uid;
            })[0];
            if (localInstance) {
                Object.assign(localInstance, instance);
            } else {
                state[source].push(instance);
            }
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
            await env.dispatch("lockUpdateManager");
            context.commit("updateOrAddInstance", instance);
            Vue.nextTick(() => {
                env.dispatch("unlockUpdateManager");
            });
            return instance;
        },
        async createInstance(context, type) {
            await env.dispatch("lockChanges");
            var instance = await api.create(type);
            context.commit("addInstance", instance);
            Vue.nextTick(() => {
                env.dispatch("unlockChanges");
            });
            return i;
        },
        async deleteInstance(context, instance) {
            context.commit("deleteInstance", instance);
            await api.delete(instance.type, instance.id, instance.uid);
        },
        async updateOrAddInstance(context, instance) {
            var localInstance = await context.dispatch("getInstanceByUid", instance.uid);
            var update = instance;
            if (localInstance) {
                update = difference(localInstance, instance);
            }
            context.commit("updateOrAddInstance", instance);
            await updateManager.proposeUpdate(update, instance);
        },
        async copyWidget(context, widget) {
            widget = await api.create(widget.type, {
                ...widget,
                x: widget.x + 5,
                y: widget.y + 5,
                id: undefined,
            });
            context.commit("addInstance", widget);
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
