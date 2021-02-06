import $ from "jquery";
import Vue from "vue";

function generateId(property, type, id) {
    return `${property}-${type}-${id}`;
}
export var Shared = new Vue({
    data: {
        settings: {}  // Settings object (models.Settings)
    }
});
export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
        this.baseUrl = "http://127.0.0.1:8000/app/api"; // TODO remove
    }
    ajax(settings) {
        return $.ajax(settings);
    }
    retrieve() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.baseUrl}/${this.urlName}/${this.id}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.baseUrl}/${this.urlName}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }

    update(data) {
        return this.ajax({
            crossDomain: true,
            type: "PUT",
            url: `${this.baseUrl}/${this.urlName}/${this.id}/`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });
    }
}

export class WidgetManager extends API {
    constructor(...api) {
        super(...api);
        this.lastState = null;
        this.refreshRate = 1000; // ms
        this.intervalId = setInterval(() => {
            if (this.lastState !== null) {
                this.update(this.lastState);
                this.lastState = null;
            }
        }, this.refreshRate);
    }
    updated(state) {
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
