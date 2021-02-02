import $ from "jquery";
function generateId(property) {
    return `${property}-${this.id}`;
}

export class API {
    constructor(urlName, id) {
        this.urlName = urlName;
        this.id = id;
    }
    ajax(settings) {
        return $.ajax(settings);
    }
    retrieve() {
        return this.ajax({
            type: "GET",
            url: `${this.urlName}/${this.id}/`,
        });
    }
    create(data) {
        return this.ajax({
            type: "POST",
            url: `${this.urlName}/`,
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
