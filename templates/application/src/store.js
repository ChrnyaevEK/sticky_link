import Vuex from "vuex";
import Vue from "vue";
import $ from "jquery";
import { env, api, updateManager, difference, deepCopy } from "./common";

Vue.use(Vuex);

export default new Vuex.Store({
    strict: true,
    state: {
        walls: null,
        widgets: null,
        user: null,
        requestedWall: null, // Will be set from fetch widgets for anonymous access
        app: {
            title: process.env.VUE_APP_TITLE,
        },
    },
    mutations: {
        setUser(state, user) {
            if (user.is_anonymous) {
                user.username = "anonymous";
            }
            state.user = user;
        },
        setWalls(state, walls) {
            for (var wall of walls) {
                wall.source = "walls";
            }
            state.walls = walls;
        },
        setRequestedWall(state, response) {
            state.requestedWall = response;
            delete state.requestedWall.widgets;
        },
        setWidgets(state, widgets) {
            for (var widget of widgets) {
                widget.source = "widgets";
            }
            state.widgets = widgets;
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
                    context.commit("setRequestedWall", response);
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
                    api.create("wall").then((wall) => {
                        context.commit("addInstance", wall);
                        Vue.nextTick(() => {
                            env.dispatch("unlockChanges");
                            resolve(wall);
                        });
                    }, reject);
                });
            });
        },
        createWidget(context, data) {
            return new Promise((resolve, reject) => {
                env.dispatch("lockChanges").then(() => {
                    api.create(data.type, data).then((response) => {
                        context.commit("addInstance", response);
                        context.dispatch("recalculateWidgets", response.wall);
                        Vue.nextTick(() => {
                            env.dispatch("unlockChanges");
                        });
                        resolve(response);
                    }, reject);
                });
            });
        },
        deleteInstance(context, instance) {
            return new Promise((resolve, reject) => {
                context.commit("deleteInstance", instance);
                api.delete(instance.type, instance.id, instance.uid).then(resolve, reject);
            });
        },
        updateOrAddInstance(context, instance) {
            return new Promise((resolve, reject) => {
                context.dispatch("getInstanceByUid", instance.uid).then((localInstance) => {
                    var update = instance;
                    if (localInstance) {
                        update = difference(localInstance, instance);
                    }
                    context.commit("updateOrAddInstance", instance);
                    return updateManager.proposeUpdate(update, instance).then(resolve, reject);
                });
            });
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
        recalculateWidgets(context, wall) {
            if (typeof wall == "number") {
                wall = context.state.walls.filter((w) => w.id == wall)[0];
            }
            var updateArray = [];
            for (var widget of context.state.widgets) {
                let update = deepCopy(widget);
                if (update.y + update.h >= wall.h) {
                    var y = wall.h - update.h;
                    update.y = y < 0 ? 0 : y;
                }
                if (update.h >= wall.h) {
                    update.h = wall.h;
                }
                var diff = difference(widget, update);
                context.commit("updateOrAddInstance", update);
                if (Object.getOwnPropertyNames(diff).length) {
                    updateArray.push(updateManager.proposeUpdate(diff, widget));
                }
            }
            return Promise.all(updateArray);
        },
        setTabTitle(context) {
            $("#tab-title").text(`${context.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
        },
        getInstanceByUid(context, uid) {
            return [...context.state.walls, ...context.state.widgets].filter((i) => i.uid == uid)[0];
        },
    },
});
