import $ from "jquery";
import Vue from "vue";
import Vuex from "vuex";
import store from "./store";

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

export var updateManager = {
    refreshRate: 200,
    queue: {
        waiter: {},
        handler: {},
    },
    updated(source, type, id) {
        return new Promise((resolve, reject) => {
            var key = `${source}${type}${id}`;

            this.queue.handler[key] = () => {
                store
                    .dispatch("filter", {
                        source,
                        type,
                        id,
                    })
                    .then((data) => {
                        api.update_partial(type, id, data[0]).then(resolve, reject);
                    });
            };
            if (!this.queue.waiter[key]) {
                this.queue.waiter[key] = setTimeout(() => {
                    delete this.queue.waiter[key];
                    this.queue.handler[key]();
                }, this.refreshRate);
            }
        });
    },
};

export var api = {
    apiHost: process.env.VUE_APP_API_HOST,
    csrfToken: getCookie("csrftoken"),
    ajax(settings) {
        var token = this.csrfToken;
        env.dispatch("savingStart");
        return $.ajax({
            headers: {
                "X-CSRFToken": token,
            },
            ...settings,
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

        lockWidgets: false,

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
        lockWidgets(state) {
            state.lockWidgets = true;
        },
        unlockWidgets(state) {
            state.lockWidgets = false;
        },
        openWidgetOptions(state, data) {
            state.editWidget = data.id;
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
        lockWidgets(context) {
            context.commit("lockWidgets");
        },
        unlockWidgets(context) {
            context.commit("unlockWidgets");
        },
    },
});

export async function sleep(milliseconds) {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export class WS {
    constructor(urlName, id) {
        this.socket = null;
        this.urlName = urlName;
        this.id = id;
        this.connectionTimeout = 1000; // ms
        this.connect();
    }
    connect() {
        this.socket = new WebSocket(`ws://${process.env.VUE_APP_HOST}/${this.urlName}/${this.id}`);
        this.socket.onmessage = (e) => {
            this.onMessage(JSON.parse(e.data));
        };
        this.socket.onclose = () => {
            this.onClose();
        };
    }
    onMessage(e) {
        console.log(e);
    }
    onClose() {
        console.error("Wall socket closed unexpectedly");
        setTimeout(() => {
            this.connect();
        }, this.connectionTimeout);
    }
}


export function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

export function generateId(property) {
    return `${this._uid}-${property}`
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
    var allFields = [...store.state.settings.widget.general_fields, ...store.state.settings.widget.position_fields, ...store.state.settings.widget.static_fields];
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
};
