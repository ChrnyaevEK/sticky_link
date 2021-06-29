import {difference, fitWidget, getById, getByUid, getReactiveCopy} from "../common";
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


const store = new Vuex.Store({
    strict: false,
    getters: {
        getWallById: (state) => (id) => {
            return getById(state.walls, id)
        },
        getPortById: (state) => (id) => {
            return getById(state.ports, id)
        },
        getContainerById: (state) => (id) => {
            return getById(state.containers, id)
        },
        getWidgetByUid: (state) => (uid) => {
            return getByUid(state.widgets, uid)
        },
        getInstanceByUid: (state) => (uid) => {
            return getReactiveCopy([
                ...state.walls,
                ...state.widgets,
                ...state.ports,
                ...state.containers,
            ].filter((i) => i.uid === uid)[0]);
        }
    },
    state: {
        user: null,
        meta: null,
        reference: null,

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
            let state = wallId === undefined ? await api.ajaxJSON({url: "state"}) : await api.retrieve("state", wallId);
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
            let local = context.getters.getInstanceByUid(instance.uid) || {};
            let update = difference(local, instance);
            if (Object.keys(update).length) {
                context.commit("updateOrAddInstance", instance);
                await um.proposeUpdate(update, instance);
            }
        },
        async uploadSource(context, {data, name, instance}) {
            return await api.upload(instance.source.id, name, data);
        },
        async removeSource(context, instance) {
            await api.delete("source", instance.source.id);
        },
        async fetchTrustedUser(context, username) {
            return await api.ajaxJSON({url: 'trusted_user?username=' + username})
        },
        async addTrustedUser(context, {username, wall}) {
            return await api.create('trusted_user?username=' + username + '&wall=' + wall)
        },
        async deleteTrustedUser(context, {username, wall}) {
            return await api.ajaxJSON({url: 'trusted_user?username=' + username + '&wall=' + wall, type: 'DELETE'})
        }
    },
});

export default store;