import $ from "jquery";
import Vue from "vue";
import Vuex from "vuex";
import store from "./store";

const transform = require("lodash.transform");
const isEqual = require("lodash.isequal");
const isArray = require("lodash.isarray");
const isObject = require("lodash.isobject");

Vue.use(Vuex);

export function difference(origObj, newObj) {
    function changes(newObj, origObj) {
        return transform(newObj, function(result, value, key) {
            if (!isEqual(value, origObj[key])) {
                result[key] =
                    !isArray(value) && isObject(value) && isObject(origObj[key]) ? changes(value, origObj[key]) : value;
            }
        });
    }
    return changes(newObj, origObj);
}

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

export var env = new Vue({
    data: {
        changesLocked: false,
        updateManagerLocked: false,
        widgetsLocked: false, // Should disable widgets actions
        openOptionsFor: null,
        edit: false,
    },
    methods: {
        lockWidgets() {
            this.widgetsLocked = true;
        },
        unlockWidgets() {
            this.widgetsLocked = false;
        },
        lockChanges() {
            this.changesLocked = true;
        },
        unlockChanges() {
            this.changesLocked = false;
        },
        lockUpdateManager() {
            this.updateManagerLocked = true;
        },
        unlockUpdateManager() {
            this.updateManagerLocked = false;
        },
        openOptions(instance) {
            this.openOptionsFor = instance;
        },
        closeOptions() {
            this.openOptionsFor = null;
        },
        openEditor() {
            this.edit = true;
        },
        closeEditor() {
            this.edit = false;
        },
        setTabTitle(context) {
            $("#tab-title").text(`${context.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
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
            // uid: new version to send
        },
        remote: {
            // uid: version from ws
        },
    },
    methods: {
        async proposeUpdate(update, { type, id, uid }) {
            // Require Type, Id, Uid
            if (this.$env.updateManagerLocked) return;
            this.handler[uid] = Object.assign({}, this.handler[uid], update); // Merge updates
            if (!this.waiter[uid]) {
                // Already waiting to push update?
                this.waiter[uid] = (async () => {
                        await sleep(this.coolDown)
                        delete this.waiter[uid];
                        var newInstance = await api.update_partial(type, id, this.handler[uid]);
                        delete this.handler[uid];
                        if (this.remote[uid] !== undefined) {
                            // Ws finished before http - resolve miss match
                            if (this.remote[uid] !== newInstance.version) await this.resolveNewVersion(newInstance);
                            delete this.remote[newInstance.uid]; // Unset remote version
                        }
                        return newInstance;
                })();
            }
            return this.waiter[uid];
        },
        async populateRemoteUpdate(event) {
            if (this.handler[event.instance.uid] !== undefined) {
                // Http is pending right now
                this.remote[event.instance.uid] = event.instance.version;
            } else {
                // Else fire off update for instance, somebody just changed it
                await this.resolveNewVersion(event.instance);
            }
        },
        async populateRemoteDestroy(event) {
            io.change(true);
            var localInstance = await store.dispatch("getInstanceByUid", event.instance.uid);
            if (localInstance) {
                store.commit("deleteInstance", localInstance);
                if (localInstance.type == "wall") {
                    env.resolveWallDeleted(localInstance);
                }
            }
            io.change(false);
        },
        async resolveNewVersion(instance) {
            io.change(true);
            var localInstance = await store.dispatch("getInstanceByUid", instance.uid);
            await store.dispatch("fetchInstance", localInstance ? localInstance : instance);
            io.change(false);
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
                if (response.responseJSON && response.responseJSON.detail) {
                    io.alert(response.responseJSON.detail, "danger");
                } else if (response.status >= 500) {
                    // Handled else were
                    io.alert("Server error occurred", "danger");
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
        expectClose: false,
    },
    methods: {
        connect(wallId) {
            this.expectClose = false;
            this.wallId = wallId;
            this.socket = new WebSocket(
                `${process.env.NODE_ENV == "production" ? "wss" : "ws"}://${process.env.VUE_APP_HOST}/wss/${wallId}`
            );
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
            if (!this.expectClose) {
                console.error("Wall socket closed unexpectedly");
                setTimeout(() => {
                    this.connect(this.wallId);
                }, this.connectionTimeout);
            }
        },
        close() {
            this.expectClose = true;
            this.socket.close();
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

export const types = {
    Wall: "wall",
    Container: "container",
    SimpleText: "simple_text",
    URL: "url",
    Counter: "counter",
    SimpleList: "simple_list",
    SimpleSwitch: "simple_switch",
};

export default {
    types,
    difference,
    generateId,
    updateManager,
    sleep,
    env,
    api,
    handleUnexpected,
};
