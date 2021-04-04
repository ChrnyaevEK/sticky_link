import Vue from "vue";
import $ from "jquery";
import store from "./store";
import io from "./io";

export default new Vue({
    data: {
        changesLocked: false, // Look resizing, dragging, instance mutations

        openOptionsFor: null,
        edit: false,

        wallId: null,
        containerId: null,
    },
    computed: {
        wall() {
            return store.state.walls ? store.state.walls.filter((w) => w.id == this.wallId)[0] : null;
        },
        container() {
            return store.state.containers ? store.state.containers.filter((c) => c.id == this.containerId)[0] : null;
        },
    },
    methods: {
        async lockChanges() {
            this.changesLocked = true;
            await new Promise((resolve) => {
                Vue.nextTick(resolve);
            });
        },
        async unlockChanges() {
            this.changesLocked = false;
            await new Promise((resolve) => {
                Vue.nextTick(resolve);
            });
        },
        async openOptions(instance) {
            this.openOptionsFor = instance;
            await new Promise((resolve) => {
                Vue.nextTick(resolve);
            });
        },
        async closeOptions() {
            this.openOptionsFor = null;
            await new Promise((resolve) => {
                Vue.nextTick(resolve);
            });
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
