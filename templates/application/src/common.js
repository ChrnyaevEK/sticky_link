import $ from "jquery";
function generateId(property) {
    return `${property}-${this.id}`;
}

export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
        this.baseUrl = 'http://127.0.0.1:8000/'
    }
    ajax(settings) {
        return $.ajax(settings);
    }
    retrieve() {
        return this.ajax({
            crossDomain: true,
            type: "GET",
            url: `${this.baseUrl}${this.urlName}/${this.id}/`,
        });
    }
    create(data) {
        return this.ajax({
            crossDomain: true,
            type: "POST",
            url: `${this.baseUrl}${this.urlName}/`,
            data,
        });
    }
}

export function registerIdSystem(vm) {
    vm._ = function(property) {
        return generateId.call(vm, property);
    };
}

export default {
    registerIdSystem,
    API,
};
