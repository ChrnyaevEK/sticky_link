import Vue from "vue";
import $ from "jquery";
import store from "./store";
import io from "./io";

export default new Vue({
    data: {
        changesLocked: false, // Look resizing, dragging, instance mutations
        widgetsLocked: false, // Should disable widgets actions

        openOptionsFor: null,
        edit: false,
    },
    methods: {
        async lockWidgets() {
            this.widgetsLocked = true;
            await Vue.nextTick();
        },
        async unlockWidgets() {
            this.widgetsLocked = false;
            await Vue.nextTick();
        },
        async lockChanges() {
            this.changesLocked = true;
            await Vue.nextTick();
        },
        async unlockChanges() {
            this.changesLocked = false;
            await Vue.nextTick();
        },
        async openOptions(instance) {
            this.openOptionsFor = instance;
            await Vue.nextTick();
        },
        async closeOptions() {
            this.openOptionsFor = null;
            await Vue.nextTick();
        },
        setTabTitle() {
            $("#tab-title").text(`${store.state.user.username} @ ${process.env.VUE_APP_TITLE}`);
        },
        handleUnexpected() {
            io.alert("Something went wrong...", "danger");
        },
        handleBadRequest(response) {
            if (response.responseJSON && response.responseJSON.detail) {
                io.alert(response.responseJSON.detail, "danger");
            } else if (response.status >= 500) {
                io.alert("Server error occurred", "danger");
            }
        },
        makeMutable(...instances) {
            // To allow straight mutations
            return Object.assign({}, ...instances);
        },
    },
});
