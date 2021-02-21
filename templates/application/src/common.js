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
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
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
            url: `${this.apiHost}${this.urlName}/${this.id || id}/`,
        });
    }
    list() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.apiHost}${this.urlName}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.apiHost}${this.urlName}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    update(data, id) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.apiHost}${this.urlName}/${this.id || id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    delete(id) {
        return this.ajax({
            crossDomain: true,
            type: "DELETE",
            url: `${this.apiHost}${this.urlName}/${this.id || id}/`,
        });
    }
}

export class UpdateManager extends API {
    // Push data about widget at certain rate (so we do not spam server)
    constructor(urlName, id, resolve, reject) {
        super(urlName, id);
        this.lastState = null;
        this.refreshRate = 1000; // ms
        this.intervalId = setInterval(() => {
            // Grab last state and push it to server
            if (this.lastState !== null) {
                this.update(this.lastState).then(
                    resolve || function() {},
                    reject || function() {}
                );
                this.lastState = null;
            }
        }, this.refreshRate);
    }
    updated(state) {
        // Set last state
        this.lastState = deepCopy(state);
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
                $("#tab-title").text(
                    `${this.user.username} @ ${process.env.VUE_APP_TITLE}`
                );
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

export default {
    registerIdSystem,
    API,
    UpdateManager,
    Context,
};
