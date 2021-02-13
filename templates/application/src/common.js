import $ from "jquery";
import Vue from "vue";

function generateId(property, type, id) {
    return `${property}-${type}-${id}`;
}
export var Shared = new Vue({
    data: {
        settings: {}, // Settings object (models.Settings)
        user: {
            username: undefined,
            email: undefined,
        },
        saving: false,  // Global saving indicator
        saved: false,  // Global safe indicator
        savedTimeoutId: undefined,
        savedTimeoutDuration: 2000,  // ms, until property will be unset
    },
    methods: {
        init() {
            var api = new API("user");
            return api.list().then((response) => {
                var user = response.pop();
                this.$set(this, "user", user);
                this.$set(this, "settings", user.settings);
            });
        },
    },
    watch: {
        saved(val){
            if (val){
                this.saving = false
                if (this.savedTimeoutId) clearTimeout(this.savedTimeoutId)
                this.savedTimeoutId = setTimeout(()=>{
                    this.saved = false
                    this.savedTimeoutId = undefined
                }, this.savedTimeoutDuration)                
            }
        },
        saving(val){
            if (val){
                this.saved = false
            }
        }
    }
});
export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
        // this.baseUrl = "http://127.0.0.1:8000/app/api/"; // TODO remove
        this.baseUrl = "/app/api/"; // TODO remove
        this.csrfCookieName = 'csrftoken'
        this.csrfToken = this.getCookie(this.csrfCookieName)
    }
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    ajax(settings) {
        var token = this.csrfToken
        return $.ajax({
            headers: {
                'X-CSRFToken': token
            },
            ...settings
        });
    }
    retrieve() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.baseUrl}${this.urlName}/${this.id}/`,
        });
    }
    list() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.baseUrl}${this.urlName}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.baseUrl}${this.urlName}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    update(data) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.baseUrl}${this.urlName}/${this.id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    delete() {
        return this.ajax({
            crossDomain: true,
            type: "DELETE",
            url: `${this.baseUrl}${this.urlName}/${this.id}/`,
        });
    }
}

export class WidgetManager extends API {
    // Push data about widget at certain rate (so we do not spam server)
    constructor(urlName, id, resolve, reject) {
        super(urlName, id);
        this.lastState = null;
        this.refreshRate = 1000; // ms
        this.intervalId = setInterval(() => {
            // Grab last state and push it to server
            if (this.lastState !== null) {
                Shared.saving = true
                this.update(this.lastState).then(()=>{
                    Shared.saved = true
                    resolve()
                }, reject);
                this.lastState = null;
            }
        }, this.refreshRate);
    }
    updated(state) {
        // Set last state
        this.lastState = deepCopy(state);
    }
}
export function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

export function registerIdSystem(vm, type, id) {
    vm._ = function(property) {
        return generateId.call(vm, property, type, id);
    };
}

export default {
    registerIdSystem,
    API,
    WidgetManager,
    Shared,
};
