import Vue from "vue";
import um from "./um";
import { sleep } from "../common";

export default new Vue({
    data: {
        wallId: null,
        socket: null,
        reopenTime: 1000,
    },
    methods: {
        open(wallId) {
            if (this.socket !== null) {
                this.socket.onclose = () => {};
                this.socket.close();
            }
            this.wallId = wallId;
            this.socket = new WebSocket(
                `${process.env.NODE_ENV == "production" ? "wss" : "ws"}://${process.env.VUE_APP_HOST}/wss/${wallId}`
            );
            this.socket.onmessage = (e) => {
                this.onMessage(e);
            };
            this.socket.onclose = (e) => {
                this.onClose(e);
            };
        },
        onMessage(event) {
            event = JSON.parse(event.data);
            switch (event.type) {
                case "on_instance_update":
                    um.populateRemoteUpdate(event);
                    break;
                case "on_instance_destroy":
                    um.populateRemoteDestroy(event);
                    break;
            }
        },
        async onClose() {
            console.error("Wall socket closed unexpectedly");
            await sleep(this.reopenTime);
            this.open(this.wallId);
        },
    },
});
