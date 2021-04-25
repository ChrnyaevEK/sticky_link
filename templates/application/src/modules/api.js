import $ from "jquery";
import env from "./env";

var csrfToken = (function getCookie(name) {
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
})("csrftoken");

export default {
    async ajax(settings) {
        try {
            return await $.ajax({
                ...settings,
                data: settings.data ? JSON.stringify(settings.data) : undefined,
                crossDomain: true,
                contentType: "application/json",
                dataType: "json",
                processData: false,
                url: process.env.VUE_APP_API_HOST + "/" + settings.url + "/",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
            });
        } catch (response) {
            env.handleBadRequest(response);
            throw response;
        }
    },
    get(type) {
        return this.ajax({ url: type });
    },
    retrieve(type, id) {
        return this.ajax({ url: type + "/" + id });
    },
    list(type) {
        return this.ajax({ url: type });
    },
    create(type, data) {
        return this.ajax({
            type: "POST",
            url: type,
            data,
        });
    },
    update(type, id, data) {
        return this.ajax({
            type: "PUT",
            url: type + "/" + id,
            data,
        });
    },
    update_partial(type, id, data) {
        return this.ajax({
            type: "PATCH",
            url: type + "/" + id,
            data,
        });
    },
    delete(type, id) {
        return this.ajax({
            type: "DELETE",
            url: type + "/" + id,
        });
    },
};
