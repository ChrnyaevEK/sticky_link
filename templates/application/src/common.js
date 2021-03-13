import $ from "jquery";
import Vue from "vue";
import Vuex from "vuex";
import store from "./store";
import router from "./router";

Vue.use(Vuex);

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
                    return api.update_partial(instance.type, instance.id, instance).then((response) => {
                        if (this.remote[response.uid] !== undefined) {
                            // Ws finished before http - resolve miss match
                            if (this.remote[response.uid] !== response.version) {
                                this.resolveNewVersion(response);
                            }
                            delete this.remote[response.uid]; // Unset remote version
                        }
                        resolve(response);
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
            store.dispatch("getInstanceByUid", update.instance.uid).then((localInstance) => {
                if (localInstance) {
                    store.commit("deleteInstance", localInstance);
                    if (localInstance.type == "wall") {
                        env.dispatch("resolveWallDeleted");
                    }
                }
            });
        },
        resolveNewVersion(instance) {
            store.dispatch("getInstanceByUid", instance.uid).then((localInstance) => {
                if (localInstance) {
                    store.dispatch("fetchInstance", localInstance);
                } else {
                    store.dispatch("fetchInstance", instance);
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

export function handleUnexpected(){
    env.dispatch("showAlert", {
        msg: "Something went wrong...",
        klass: "danger",
    })
}

export var api = {
    apiHost: process.env.VUE_APP_API_HOST,
    csrfToken: getCookie("csrftoken"),
    ajax(settings) {
        var token = this.csrfToken;
        env.dispatch("savingStart");
        return $.ajax({
            ...settings,
            headers: {
                "X-CSRFToken": token,
            },
        }).always(() => {
            env.dispatch("savingStop");
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

export var env = new Vuex.Store({
    state: {
        loadingState: null,
        loadingStates: {
            loading: true,
            ready: false,
        },

        savingState: null,
        savingStates: {
            saving: "Saving...",
            saved: "Saved",
            idle: "Auto save",
        },
        savingTimeoutId: null,
        savingTimeoutDuration: 5000,

        alertShow: false,
        alertMessage: null,
        alertClass: "info",

        lockChanges: false,
        lockUpdateManager: false,

        editWidget: null,
    },
    mutations: {
        setSaved(state) {
            state.savingState = state.savingStates.saved;
        },
        setSaving(state) {
            state.savingState = state.savingStates.saving;
        },
        setSavingIdle(state) {
            state.savingState = state.savingStates.idle;
            state.savingTimeoutId = null;
        },
        setSavingTimeoutId(state, id) {
            state.savingTimeoutId = id;
        },
        setAlert(state, data) {
            state.alertClass = data.alertClass;
            state.alertMessage = data.alertMessage;
            state.alertShow = true;
        },
        unsetAlert(state) {
            state.alertClass = "info";
            state.alertMessage = null;
            state.alertShow = false;
        },
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
        savingStart(context) {
            context.commit("setSaving");
        },
        savingStop(context) {
            context.commit("setSaved");
            clearTimeout(context.state.savingTimeoutId);
            context.commit(
                "setSavingTimeoutId",
                setTimeout(() => {
                    context.commit("setSavingIdle");
                }, context.state.savingTimeoutDuration)
            );
        },
        showAlert(context, { msg, klass }) {
            context.commit("setAlert", {
                alertMessage: msg,
                alertClass: klass,
            });
        },
        hideAlert(context) {
            context.commit("unsetAlert");
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
        resolveWallDeleted(context) {
            router.push({
                name: "appEmpty",
            });
            context.dispatch("showAlert", {
                msg: "Wall has been deleted!",
                klass: "success",
            });
        },
    },
});

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
};
