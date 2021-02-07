import $ from "jquery";
import Vue from "vue";

function generateId(property, type, id) {
    return `${property}-${type}-${id}`;
}
export var Shared = new Vue({
    data: {
        settings: {},  // Settings object (models.Settings)
        user: {
            username: 'Unknown',
            email: 'Unknown',
            id: 'Unknown'
        },
    },
    methods: {
        init(){
            var api = new API()
            return api.ajax({
                crossDomain: true,
                type: "GET",
                contentType: "application/json",
                url: `${api.baseUrl}app/profile/`,
            }).then((response)=>{
                this.$set(this, 'settings', response.settings)
                this.$set(this, 'user', response.user)
            })
        }
    }
});
export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
        this.baseUrl = "http://127.0.0.1:8000/"; // TODO remove
    }
    ajax(settings) {
        return $.ajax(settings);
    }
    retrieve() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.baseUrl}app/api/${this.urlName}/${this.id}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.baseUrl}app/api/${this.urlName}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    update(data) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.baseUrl}app/api/${this.urlName}/${this.id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
    delete(){
        return this.ajax({
            crossDomain: true,
            type: "DELETE",
            url: `${this.baseUrl}app/api/${this.urlName}/${this.id}/`,
        });
    }
}

export class WidgetManager extends API {
    // Push data about widget at certain rate (so we do not spam server)
    constructor(urlName, id, resolve, reject) {
        super(urlName, id);
        this.reject = reject  // Will vbe passed as reject function to promise
        this.resolve = resolve  // Will vbe passed as resolve function to promise
        this.lastState = null;
        this.refreshRate = 1000; // ms
        this.intervalId = setInterval(() => {  // Grab last state and push it to server
            if (this.lastState !== null) {
                this.update(this.lastState).then(resolve, reject)
                this.lastState = null;
            }
        }, this.refreshRate);
    }
    updated(state) {  // Set last state
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
