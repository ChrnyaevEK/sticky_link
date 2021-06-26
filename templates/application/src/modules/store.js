import {difference, fitWidget} from "../common";
import Vuex from "vuex";
import Vue from "vue";
import api from "./api";
import um from "./um";

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

function getInstanceByUid(uid) {
    return [
        ...store.state.walls,
        ...store.state.widgets,
        ...store.state.ports,
        ...store.state.containers,
    ].filter((instance) => instance.uid === uid)[0];
}

const store = new Vuex.Store({
    strict: true,
    state: {
        user: null,
        meta: null,

        ports: [],
        walls: [],
        containers: [],
        widgets: [],

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
                if (state[source][i].uid === instance.uid) {
                    return state[source].splice(i, 1);
                }
            }
        },
        updateOrAddInstance(state, instance) {
            let source = determineSource(instance);
            for (let local of state[source]) {
                if (local.uid === instance.uid) {
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
            instance = await api.create(instance.type, instance);
            context.commit("updateOrAddInstance", instance);
            return instance;
        },
        async deleteInstance(context, instance) {
            await um.cancelPending(instance); // cancel or wait for pending update
            await api.delete(instance.type, instance.id, instance.uid); // Perform delete
            context.commit("deleteInstance", instance); // Delete local copy
        },
        async recalculateWidgets(context, container) {
            let update = [];
            for (let widget of context.state.widgets) {
                if (widget.container === container.id) {
                    widget = fitWidget(Object.assign({}, widget), container);
                    update.push(context.dispatch("updateOrAddInstance", widget));
                }
            }
            await Promise.all(update);
        },
        async updateOrAddInstance(context, instance) {
            let local = getInstanceByUid(instance.uid) || {};
            let update = difference(local, instance);
            if (Object.keys(update).length) {
                context.commit("updateOrAddInstance", instance);
                instance = await um.proposeUpdate(update, instance);
            }
            return instance;
        },
        async uploadSource(context, {data, name, instance}) {
            return await api.upload(instance.source.id, name, data);
        },
        async removeSource(context, instance) {
            await api.delete("source", instance.source.id);
        },
    },
});

export default store;