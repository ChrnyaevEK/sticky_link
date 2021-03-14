import $ from "jquery";
import Vue from "vue";
import Vuex from "vuex";
import store from "./store";
import router from "./router";

Vue.use(Vuex);
var Rollbar = require("rollbar");
export var rollbar = new Rollbar({
    accessToken: "352f084b3c4b4a60951b25ce2252fb6f",
    captureUncaught: process.env.NODE_ENV == "production",
    captureUnhandledRejections: process.env.NODE_ENV == "production",
    payload: {
        environment: "production"
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export var io = new Vue({
    data: {
        alertUtil: {
            html: null,
            type: null,
            visible: false,
        },
        saveUtil: {
            state: null,
            type: null,
            states: {
                saving: "Processing...",
                saved: "Saved",
                idle: "Auto save",
            },
            timeoutId: null,
            timeoutDuration: 5000,
        },
        changeUtil: {
            state: null,
            states: {
                newVersionAvailable: "The wall has changed",
                lastVersion: null,
            },
            timeoutId: null,
            timeoutDuration: 1000,
        },
    },
    methods: {
        alert(html, type) {
            this.alertUtil.html = html;
            this.alertUtil.type = type;
            this.alertUtil.visible = true;
        },
        save(active) {
            if (active) {
                this.saveUtil.state = this.saveUtil.states.saving;
            } else {
                clearTimeout(this.saveUtil.timeoutId);
                this.saveUtil.state = this.saveUtil.states.saved;
                this.saveUtil.type = "success";
                this.saveUtil.timeoutId = setTimeout(() => {
                    this.saveUtil.state = this.saveUtil.states.idle;
                    this.saveUtil.type = null;
                }, this.saveUtil.timeoutDuration);
            }
        },
        change(active) {
            if (active) {
                this.changeUtil.state = this.changeUtil.states.newVersionAvailable;
            } else {
                clearTimeout(this.changeUtil.timeoutId);
                this.changeUtil.timeoutId = setTimeout(() => {
                    this.changeUtil.state = this.changeUtil.states.lastVersion;
                }, this.changeUtil.timeoutDuration);
            }
        },
    },
});

export var env = new Vuex.Store({
    state: {
        lockChanges: false,
        lockUpdateManager: false,

        editWidget: null,
    },
    mutations: {
        lockChanges(state) {
            state.lockChanges = true;
        },
        unlockChanges(state) {
            state.lockChanges = false;
        },
        lockUpdateManager(state) {
            state.lockUpdateManager = true;
        },
        unlockUpdateManager(state) {
            state.lockUpdateManager = false;
        },
        openWidgetOptions(state, data) {
            state.editWidget = data;
        },
        closeWidgetOptions(state) {
            state.editWidget = null;
        },
    },
    actions: {
        openWidgetOptions(context, data) {
            context.commit("openWidgetOptions", data);
        },
        closeWidgetOptions(context) {
            context.commit("closeWidgetOptions");
        },
        lockChanges(context) {
            context.commit("lockChanges");
        },
        unlockChanges(context) {
            context.commit("unlockChanges");
        },
        lockUpdateManager(context) {
            context.commit("lockUpdateManager");
        },
        unlockUpdateManager(context) {
            context.commit("unlockUpdateManager");
        },
        resolveWallDeleted(context, wall) {
            io.alert(`Wall <strong>${wall.title}</strong> has been deleted!`, "success");
            router.push({
                name: "appEmpty",
            });
        },
        resolveWallCreated(context, wall) {
            io.alert("New wall has been created!", "success");
            router.push({
                name: "wallEdit",
                params: {
                    wallId: wall.id,
                },
            });
        },
    },
});

export var updateManager = new Vue({
    data: {
        coolDown: 1000,
        waiter: {
            // uid: timeout id
        },
        handler: {
            // uid: function to call real update
        },
        remote: {
            // uid: version from ws
        },
    },
    methods: {
        proposeUpdate(instance) {
            // Require Type, Id, Uid
            return new Promise((resolve, reject) => {
                if (env.state.lockUpdateManager) {
                    return resolve();
                }
                var update = () => {
                    return api.update_partial(instance.type, instance.id, instance).then((newInstance) => {
                        if (this.remote[newInstance.uid] !== undefined) {
                            // Ws finished before http - resolve miss match
                            if (this.remote[newInstance.uid] !== newInstance.version) {
                                this.resolveNewVersion(newInstance);
                            }
                            delete this.remote[newInstance.uid]; // Unset remote version
                        }
                        resolve(newInstance);
                    }, reject);
                };

                this.handler[instance.uid] = update;
                clearTimeout(this.waiter[instance.uid]); // Unset last update
                this.waiter[instance.uid] = setTimeout(() => {
                    this.handler[instance.uid]().then(() => {
                        delete this.handler[instance.uid], this.waiter[instance.uid];
                    }); // Call real update
                }, this.coolDown);
            });
        },
        populateRemoteUpdate(update) {
            if (this.handler[update.instance.uid] !== undefined) {
                // Http is pending right now
                this.remote[update.instance.uid] = update.instance.version;
            } else {
                // Else fire off update for instance, somebody just changed it
                this.resolveNewVersion(update.instance);
            }
        },
        populateRemoteDestroy(update) {
            io.change(true);
            store.dispatch("getInstanceByUid", update.instance.uid).then((localInstance) => {
                if (localInstance) {
                    store.commit("deleteInstance", localInstance);
                    if (localInstance.type == "wall") {
                        env.dispatch("resolveWallDeleted");
                    }
                }
                io.change(false);
            });
        },
        resolveNewVersion(instance) {
            io.change(true);
            return store.dispatch("getInstanceByUid", instance.uid).then((localInstance) => {
                if (localInstance) {
                    store.dispatch("fetchInstance", localInstance).then(() => {
                        io.change(false);
                    });
                } else {
                    store.dispatch("fetchInstance", instance).then(() => {
                        io.change(false);
                    });
                }
            });
        },
    },
});

export class DefaultDict {
    constructor(defaultVal) {
        return new Proxy(
            {},
            {
                get: (target, name) => (name in target ? target[name] : defaultVal),
            }
        );
    }
}

export function handleUnexpected() {
    io.alert("Something went wrong...", "danger");
}

export var api = {
    apiHost: process.env.VUE_APP_API_HOST,
    csrfToken: getCookie("csrftoken"),
    ajax(settings) {
        var token = this.csrfToken;
        io.save(true);
        return $.ajax({
            ...settings,
            headers: {
                "X-CSRFToken": token,
            },
        })
            .fail((response) => {
                if (response.responseJSON.detail) {
                    io.alert(response.responseJSON.detail, "danger");
                }
            })
            .always(() => {
                io.save(false);
            });
    },
    get(path) {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}/${path}/`,
        });
    },
    retrieve(type, id) {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}/${type}/${id}/`,
        });
    },
    list(type) {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}/${type}/`,
        });
    },
    create(type, data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.apiHost}/${type}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    },
    update(type, id, data) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.apiHost}/${type}/${id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    },
    update_partial(type, id, data) {
        return this.ajax({
            crossDomain: true,
            type: "PATCH",
            url: `${this.apiHost}/${type}/${id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    },
    delete(type, id) {
        return this.ajax({
            crossDomain: true,
            type: "DELETE",
            url: `${this.apiHost}/${type}/${id}/`,
        });
    },
};

export var ws = new Vue({
    data: {
        wallId: null,
        socket: null,
        connectionTimeout: 1000,
    },
    methods: {
        connect(wallId) {
            this.wallId = wallId;
            this.socket = new WebSocket(`ws://${process.env.VUE_APP_HOST}/wall/${wallId}`);
            this.socket.onmessage = (e) => {
                this.onMessage(e);
            };
            this.socket.onclose = (e) => {
                this.onClose(e);
            };
        },
        onMessage(e) {
            var event = JSON.parse(e.data);
            if (event.type == "on_instance_update") {
                updateManager.populateRemoteUpdate(event);
            } else if (event.type == "on_instance_destroy") {
                updateManager.populateRemoteDestroy(event);
            }
        },
        onClose() {
            console.error("Wall socket closed unexpectedly");
            setTimeout(() => {
                this.connect(this.wallId);
            }, this.connectionTimeout);
        },
    },
});

export async function sleep(milliseconds) {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

export function generateId(property) {
    return `${this._uid}-${property}`;
}

export function widgetGenerateUpdate(widget, fields) {
    var update = {};
    for (var field of fields) {
        update[field] = widget[field];
    }
    return update;
}

export function widgetGenerateDifference(newWidget, oldWidget) {
    var leftFields = [];
    var fieldGroups = [store.state.settings.widget.general_fields, store.state.settings.widget.position_fields];
    var allFields = [
        ...store.state.settings.widget.general_fields,
        ...store.state.settings.widget.position_fields,
        ...store.state.settings.widget.static_fields,
    ];
    for (let field of Object.getOwnPropertyNames(newWidget)) {
        if (allFields.indexOf(field) == -1) {
            leftFields.push(field);
        }
    }
    fieldGroups.push(leftFields);
    for (let fields of fieldGroups) {
        for (let field of fields) {
            if (oldWidget[field] !== newWidget[field]) {
                return widgetGenerateUpdate(newWidget, fields);
            }
        }
    }
    return {};
}

export function widgetApplyUpdate(widget, source, fields) {
    for (var field of fields) {
        widget[field] = source[field];
    }
}

export default {
    widgetApplyUpdate,
    generateId,
    updateManager,
    sleep,
    env,
    api,
    handleUnexpected,
    rollbar,
};
