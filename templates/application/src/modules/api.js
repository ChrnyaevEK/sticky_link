import $ from "jquery";
import Vue from "vue";

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
                crossDomain: true,
                processData: false,
                url: process.env.VUE_APP_API_PROTOCOL + '://' + process.env.VUE_APP_HOST + settings.url,
                headers: {
                    "X-CSRFToken": csrfToken,
                    ...(settings.headers || {}),
                },
            });
        } catch (response) {
            if (response.responseJSON && response.responseJSON.detail) {
                Vue.notify({
                    text: response.responseJSON.detail,
                    type: "error",
                });
            } else if (response.status >= 500) {
                Vue.notify({
                    text: "Server error occurred",
                    type: "error",
                });
            }
            throw response
        }
    },
    ajaxJSON(settings, api) {
        api = api === undefined
        if (api) {
            settings.url = process.env.VUE_APP_API + "/" + settings.url
        }
        return this.ajax({
            ...settings,
            data: settings.data ? JSON.stringify(settings.data) : undefined,
            contentType: "application/json",
            dataType: "json",
        });
    },
    get(type) {
        return this.ajaxJSON({url: type});
    },
    retrieve(type, id) {
        return this.ajaxJSON({url: type + "/" + id});
    },
    list(type) {
        return this.ajaxJSON({url: type});
    },
    create(type, data) {
        return this.ajaxJSON({
            type: "POST",
            url: type,
            data,
        });
    },
    update(type, id, data) {
        return this.ajaxJSON({
            type: "PUT",
            url: type + "/" + id,
            data,
        });
    },
    updatePartial(type, id, data) {
        return this.ajaxJSON({
            type: "PATCH",
            url: type + "/" + id,
            data,
        });
    },
    delete(type, id) {
        return this.ajaxJSON({
            type: "DELETE",
            url: type + "/" + id,
        });
    },
    upload(id, name, data) {
        return this.ajax({
            url: "source/" + id,
            type: "PUT",
            cache: false,
            contentType: false,
            data,
            headers: {
                "Content-Disposition": 'attachment; filename="' + name + '"',
            },
        });
    },
};
