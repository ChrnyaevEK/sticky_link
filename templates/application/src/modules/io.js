import Vue from "vue";

export default new Vue({
    data: {
        alertUtil: {
            html: null,
            type: null,
            visible: false,
            fadeOutCoolDown: 1000,
        },
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
    },
    methods: {
        alert(html, type) {
            this.alertUtil.html = html;
            this.alertUtil.type = type;
            this.alertUtil.visible = true;
        },
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
    },
});
