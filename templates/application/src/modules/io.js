import Vue from "vue";
import $ from "jquery";

export default new Vue({
    data: {
        saveUtil: {
            state: null,
            type: null,
            states: {
                saving: "Processing...",
                saved: "Saved",
                idle: "Auto save",
            },
            timeoutId: null,
            timeoutDuration: 5000,
        },
        changeUtil: {
            state: false,
            states: {
                synchronizing: true,
                synchronized: false,
            },
            timeoutId: null,
            timeoutDuration: 1000,
        },
        warning: {
            class: 'response-warning',
        }
    },
    methods: {
        save(active) {
            if (active) {
                this.saveUtil.state = this.saveUtil.states.saving;
            } else {
                clearTimeout(this.saveUtil.timeoutId);
                this.saveUtil.state = this.saveUtil.states.saved;
                this.saveUtil.type = "success";
                this.saveUtil.timeoutId = setTimeout(() => {
                    this.saveUtil.state = this.saveUtil.states.idle;
                    this.saveUtil.type = null;
                }, this.saveUtil.timeoutDuration);
            }
        },
        change(active) {
            if (active) {
                this.changeUtil.state = this.changeUtil.states.synchronizing;
            } else {
                clearTimeout(this.changeUtil.timeoutId);
                this.changeUtil.timeoutId = setTimeout(() => {
                    this.changeUtil.state = this.changeUtil.states.synchronized;
                }, this.changeUtil.timeoutDuration);
            }
        },
        setWarning(response, target) {
            this.unsetWarning(target);
            for (var [field, error] of Object.entries(response.responseJSON)) {
                error = $(`<p class="${this.warning.class} col-12 text-danger">${error[0]}</p>`);
                target.find(`[for*="${field}"]`)
                    .addClass(`text-danger ${this.warning.class}`)
                    .closest("div")
                    .append(error);
            }
        },
        unsetWarning(target) {
            target.find(`.${this.warning.class}`).removeClass("text-danger").removeClass(this.warning.class);
            target.find(`p.${this.warning.class}`).remove();
        },
    },
});
