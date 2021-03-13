import Vuex from "vuex";
import Vue from "vue";
import $ from "jquery";
import { api, updateManager, env } from "./common";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        walls: null,
        widgets: null,
        user: null,
        settings: null,
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setWalls(state, walls) {
            for (var wall of walls) {
                wall.source = "walls";
            }
            state.walls = walls;
        },
        setWidgets(state, widgets) {
            for (var widget of widgets) {
                widget.source = "widgets";
            }
            state.widgets = widgets;
        },
        setSettings(state, settings) {
            state.settings = settings;
        },
        deleteInstance(state, instance) {
            for (var i = 0; i < state[instance.source].length; i++) {
                if (state[instance.source][i].uid == instance.uid) {
                    state[instance.source].splice(i, 1);
                    break;
                }
            }
        },
        updateOrAddInstance(state, instance) {
            if (instance.source == undefined) {
                instance.source = instance.type == "wall" ? "walls" : "widgets";
            }
            var localInstance = state[instance.source].filter((i) => {
                return i.uid == instance.uid;
            })[0];
            if (localInstance) {
                Object.assign(localInstance, instance);
            } else {
                state[instance.source].push(instance);
            }
        },
        addInstance(state, instance) {
            instance.source = instance.type == "wall" ? "walls" : "widgets";
            state[instance.source].push(instance);
        },
        recalculateWidgets(state, newWall) {
            var wall = state.walls.filter((wall) => wall.id == newWall.id)[0];
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
                    context.commit("setWidgets", response.widgets);
                    resolve();
                }, reject);
            });
        },
        fetchInstance(context, data) {
            return new Promise((resolve, reject) => {
                api.retrieve(data.type, data.id).then((response) => {
                    response.source = data.source;
                    env.dispatch("lockUpdateManager").then(() => {
                        context.commit("updateOrAddInstance", response);
                        Vue.nextTick(() => {
                            env.dispatch("unlockUpdateManager");
                        });
                    });
                    resolve(response);
                }, reject);
            });
        },
        createWall(context) {
            return new Promise((resolve, reject) => {
                env.dispatch("lockChanges").then(() => {
                    api.create("wall").then((response) => {
                        context.commit("addInstance", response);
                        Vue.nextTick(() => {
                            env.dispatch("unlockChanges");
                        });
                        resolve(response);
                    }, reject);
                });
            });
        },
        validateWall(context, data) {
            return context.state.walls.some((wall) => String(wall.id) == data.id);
        },
        createWidget(context, data) {
            return new Promise((resolve, reject) => {
                env.dispatch("lockChanges").then(() => {
                    api.create(data.type, data).then((response) => {
                        context.commit("addInstance", response);
                        Vue.nextTick(() => {
                            env.dispatch("unlockChanges");
                        });
                        resolve(response);
                    }, reject);
                });
            });
        },
        deleteInstance(context, data) {
            return new Promise((resolve, reject) => {
                context.commit("deleteInstance", data);
                api.delete(data.type, data.id).then(resolve, reject);
            });
        },
        updateOrAddInstance(context, data) {
            context.commit("updateOrAddInstance", data);
            return updateManager.proposeUpdate(data);
        },
        copyWidget(context, data) {
            return new Promise((resolve, reject) => {
                api.create(data.type, {
                    ...data,
                    x: data.x + 5,
                    y: data.y + 5,
                    id: undefined,
                }).then((response) => {
                    context.commit("addInstance", response);
                    resolve();
                }, reject);
            });
        },
        validateWidget(context, data) {
            return context.state.widgets.some((widget) => String(widget.id) == data.id && widget.type == data.type);
        },
        recalculateWidgets(context, data) {
            context.commit("recalculateWidgets", data);
        },
        setTabTitle(context) {
            $("#tab-title").text(`${context.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
        },
        getInstanceByUid(context, uid) {
            return [...context.state.walls, ...context.state.widgets].filter((i) => i.uid == uid)[0];
        },
    },
});
