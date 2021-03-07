import Vuex from "vuex";
import Vue from "vue";
import $ from "jquery";
import { api, updateManager } from "./common";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        walls: null,
        widgets: null,
        user: null,
        settings: null,
    },
    mutations: {
        setUser(state, data) {
            state.user = data;
        },
        setWalls(state, data) {
            state.walls = data;
        },
        setWidgets(state, data) {
            state.widgets = data;
        },
        setSettings(state, data) {
            state.settings = data;
        },
        deleteWall(state, data) {
            for (var i = 0; i < state.walls.length; i++) {
                if (state.walls[i].id == data.id) {
                    state.walls.splice(i, 1);
                    break;
                }
            }
        },
        updateWall(state, data) {
            Object.assign(
                state.walls.filter((wall) => {
                    return wall.id == data.id;
                })[0],
                data
            );
        },
        addWall(state, data) {
            state.walls.push(data);
        },
        deleteWidget(state, data) {
            for (var i = 0; i < state.widgets.length; i++) {
                var widget = state.widgets[i];
                if (widget.id == data.id && widget.type == data.type) {
                    state.widgets.splice(i, 1);
                    break;
                }
            }
        },
        updateWidget(state, data) {
            Object.assign(
                state.widgets.filter((widget) => {
                    return widget.id == data.id && widget.type == data.type;
                })[0],
                data
            );
        },
        recalculateWidgets(state, data) {
            var wall = state.walls.filter((wall) => wall.id == data.id)[0];
            for (var widget of state.widgets) {
                if (widget.x + widget.w >= wall.w) {
                    var x = wall.w - widget.w;
                    widget.x = x < 0 ? 0 : x;
                }
                if (widget.y + widget.h >= wall.h) {
                    var y = wall.h - widget.h;
                    widget.y = y < 0 ? 0 : y;
                }
                if (widget.h >= wall.h) {
                    widget.h = wall.h;
                }
                if (widget.w >= wall.w) {
                    widget.w = wall.w;
                }
            }
        },
        addWidget(state, data) {
            state.widgets.push(data);
        },
    },
    actions: {
        fetchUser(context) {
            return new Promise((resolve, reject) => {
                api.get("user").then((response) => {
                    context.commit("setUser", response);
                    context.dispatch("setTabTitle");
                    resolve();
                }, reject);
            });
        },
        fetchSettings(context) {
            return new Promise((resolve, reject) => {
                api.get("settings").then((response) => {
                    context.commit("setSettings", response);
                    resolve();
                }, reject);
            });
        },
        fetchWalls(context) {
            return new Promise((resolve, reject) => {
                api.list("wall").then((response) => {
                    context.commit("setWalls", response);
                    resolve();
                }, reject);
            });
        },
        fetchWidgets(context, id) {
            return new Promise((resolve, reject) => {
                api.retrieve("wall", id).then((response) => {
                    context.commit("setWidgets", response);
                    resolve();
                }, reject);
            });
        },
        createWall(context) {
            return new Promise((resolve, reject) => {
                api.create("wall").then((response) => {
                    context.commit("addWall", response);
                    resolve(response);
                }, reject);
            });
        },
        deleteWall(context, data) {
            return new Promise((resolve, reject) => {
                api.delete("wall", data.id).then(() => {
                    context.commit("deleteWall", data);
                    resolve();
                }, reject);
            });
        },
        updateWall(context, data) {
            context.commit("updateWall", data);
            return updateManager.updated("walls", "wall", data.id);
        },
        validateWall(context, data) {
            return context.state.walls.some(
                (wall) => String(wall.id) == data.id
            );
        },
        createWidget(context, data) {
            return new Promise((resolve, reject) => {
                api.create(data.type, data).then((response) => {
                    context.commit("addWidget", response);
                    resolve(response);
                }, reject);
            });
        },
        deleteWidget(context, data) {
            return new Promise((resolve, reject) => {
                api.delete(data.type, data.id).then(() => {
                    context.commit("deleteWidget", data);
                    resolve();
                }, reject);
            });
        },
        updateWidget(context, data) {
            context.commit("updateWidget", data);
            return updateManager.updated("widgets", data.type, data.id);
        },
        copyWidget(context, data) {
            return new Promise((resolve, reject) => {
                api.create(data.type, {
                    ...data,
                    x: data.x + 5,
                    y: data.y + 5,
                    id: undefined,
                }).then((response) => {
                    context.commit("addWidget", response);
                    resolve();
                }, reject);
            });
        },
        validateWidget(context, data) {
            return context.state.widgets.some(
                (widget) =>
                    String(widget.id) == data.id && widget.type == data.type
            );
        },
        recalculateWidgets(context, data) {
            context.commit("recalculateWidgets", data);
        },
        filter(context, { source, type, id }) {
            return context.state[source].filter((i) => {
                return i.type == type && i.id == id;
            });
        },
        setTabTitle(context) {
            $("#tab-title").text(
                `${context.state.user.username} @ ${process.env.VUE_APP_TITLE}`
            );
        },
    },
});
