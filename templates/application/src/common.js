import $ from "jquery";
import Vue from "vue";

function generateId(property, type, id) {
    return `${property}-${type}-${id}`;
}

export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
        this.apiHost = process.env.VUE_APP_API_HOST;
        this.csrfCookieName = "csrftoken";
        this.csrfToken = this.getCookie(this.csrfCookieName);
    }
    getCookie(name) {
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
    ajax(settings) {
        var token = this.csrfToken;
        Context.saving = true;
        return $.ajax({
            headers: {
                "X-CSRFToken": token,
            },
            ...settings,
        }).always(() => {
            Context.saved = true;
        });
    }
    retrieve(id) {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}/${this.urlName}/${this.id || id}/`,
        });
    }
    list() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}/${this.urlName}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.apiHost}/${this.urlName}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    update(data, id) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.apiHost}/${this.urlName}/${this.id || id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    update_partial(data, id) {
        return this.ajax({
            crossDomain: true,
            type: "PATCH",
            url: `${this.apiHost}/${this.urlName}/${this.id || id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    delete(id) {
        return this.ajax({
            crossDomain: true,
            type: "DELETE",
            url: `${this.apiHost}/${this.urlName}/${this.id || id}/`,
        });
    }
}

export class WS {
    constructor(urlName, id) {
        this.socket = null;
        this.urlName = urlName
        this.id = id
        this.connectionTimeout = 1000; // ms
        this.connect();
    }
    connect() {
        this.socket = new WebSocket(`ws://${process.env.VUE_APP_HOST}/${this.urlName}/${this.id}`);
        this.socket.onmessage = (e) => {
            this.onMessage(e);
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
            this.connect()
        }, this.connectionTimeout);
    }
}

export class UpdateManager extends API {
    // TODO use watchers
    // Push data about widget at certain rate (so we do not spam server)
    constructor(urlName, id) {
        super(urlName, id);
        this.lastState = null;
        this.resolve = null;
        this.reject = null;
        this.refreshRate = 1000; // ms
        this.intervalId = setInterval(() => {
            this.flush();
        }, this.refreshRate);
    }
    flush() {
        if (this.lastState !== null) {
            this.update_partial(this.lastState).then(this.resolve || function() {}, this.reject || function() {});
            this.lastState = null;
        }
    }
    updated(newWidget, oldWidget) {
        if (!this.lastState) this.lastState = widgetGenerateDifference(newWidget, oldWidget);
    }
}

export var Context = new Vue({
    name: "Context",
    el: "#context",
    data: {
        saving: false, // Global saving indicator
        saved: false, // Global safe indicator
        savedTimeoutId: undefined,
        savedTimeoutDuration: 5000, // ms, until property will be unset
        edit: "edit",
        view: "view",
        user: {},
        settings: {},
        walls: [],
    },
    methods: {
        initUser() {
            return new API("user").list().then((response) => {
                this.$set(this, "user", response.user);
                this.$set(this, "settings", response.settings);
                this.walls = [];
                this.$set(this, "walls", response.walls);
            });
        },
    },
    watch: {
        saved(val) {
            if (val) {
                this.saving = false;
                if (this.savedTimeoutId) clearTimeout(this.savedTimeoutId);
                this.savedTimeoutId = setTimeout(() => {
                    this.saved = false;
                    this.savedTimeoutId = undefined;
                }, this.savedTimeoutDuration);
            }
        },
        saving(val) {
            if (val) {
                this.saved = false;
            }
        },
        user: {
            handler() {
                $("#tab-title").text(`${this.user.username} @ ${process.env.VUE_APP_TITLE}`);
            },
            deep: true,
        },
    },
});

export function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

export function registerIdSystem(vm, data_source) {
    vm._ = function(property) {
        return generateId.call(vm, property, data_source.type, data_source.id);
    };
}

export function validateWall(id) {
    return Context.walls.some((w) => {
        return String(w.id) == id;
    });
}

export function deleteWall(id) {
    for (var i = 0; i < Context.walls.length; i++) {
        if (Context.walls[i].id == id) {
            Context.walls.splice(i, 1);
            break;
        }
    }
}

export function updateWall(id, obj) {
    for (var wall of Context.walls) {
        if (wall.id == id) {
            Object.assign(wall, obj);
        }
    }
}

export function widgetGenerateStaticUpdate(widget) {
    // Pull out only static fields from widget
    var update = {};
    for (var field of Context.settings.widget.static_fields) {
        update[field] = widget[field];
    }
    return update;
}

export function widgetGenerateDynamicUpdate(widget) {
    var update = deepCopy(widget);
    for (var field of Context.settings.widget.static_fields) {
        delete update[field];
    }
    return update;
}

export function widgetGenerateDifference(newWidget, oldWidget) {
    for (var field of Context.settings.widget.static_fields) {
        if (oldWidget[field] !== newWidget[field]) {
            return widgetGenerateStaticUpdate(newWidget);
        }
    }
    return widgetGenerateDynamicUpdate(newWidget);
}

export function widgetApplyStaticUpdate(widget, source) {
    // Update out only static fields in widget
    for (var field of Context.settings.widget.static_fields) {
        widget[field] = source[field];
    }
}

export function widgetApplyDynamicUpdate(widget, source) {
    for (var field of Object.getOwnPropertyNames(source)) {
        if (Context.settings.widget.static_fields.indexOf(field) == -1) {
            widget[field] = source[field];
        }
    }
}

export default {
    widgetGenerateStaticUpdate,
    widgetApplyStaticUpdate,
    widgetGenerateDynamicUpdate,
    widgetApplyDynamicUpdate,
    validateWall,
    deleteWall,
    updateWall,
    registerIdSystem,
    API,
    UpdateManager,
    Context,
};
