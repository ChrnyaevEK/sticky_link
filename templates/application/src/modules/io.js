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
            timeoutDuration: 3000,
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
            if (!target) return
            target = $(target)
            this.unsetWarning(target);
            for (var [field, error] of Object.entries(response.responseJSON)) {
                error = $(`<div class="${this.warning.class} text-danger p-1"><small>${error[0]}</small></div>`);
                target.find(`[for*="${field}"]`)
                    .addClass(`text-danger ${this.warning.class}`)
                    .closest("div")
                    .append(error);
            }
        },
        unsetWarning(target) {
            if (!target) return
            target = $(target)
            target.find(`p.${this.warning.class}`).remove();
            target.find(`.${this.warning.class}`).removeClass("text-danger").removeClass(this.warning.class);
        },
    },
});
