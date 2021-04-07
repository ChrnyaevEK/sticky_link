// UM stands for "Update Manager"
import store from "./store";
import Vue from "vue";
import env from "./env";
import api from "./api";
import io from "./io";
import { sleep } from "../common";

export default new Vue({
    data: {
        coolDown: 1000,
        waiter: {
            // uid: timeout id
        },
        handler: {
            // uid: new version to send
        },
        remote: {
            // uid: version from ws
        },
    },
    methods: {
        async cancelPending(instance) {
            delete this.handler[instance.uid]; // Prevent new ajax
            await this.waiter[instance.uid]; // Wait for pending ajax
        },
        async proposeUpdate(update, instance) {
            if (env.changesLocked) return;
            this.handler[instance.uid] = Object.assign({}, this.handler[instance.uid], update); // Merge updates
            if (!this.waiter[instance.uid]) {
                // Already waiting to push update?
                this.waiter[instance.uid] = (async () => {
                    await sleep(this.coolDown);
                    delete this.waiter[instance.uid];
                    if (this.handler[instance.uid]) {
                        let remote = await api.update_partial(instance.type, instance.id, this.handler[instance.uid]);
                        if (this.remote[instance.uid] !== undefined) {
                            // Ws finished before http - resolve miss match
                            if (this.remote[instance.uid] !== remote.version) await this.resolveNewVersion(remote);
                            delete this.remote[remote.uid]; // Unset remote version
                        }
                        delete this.handler[instance.uid];
                        return remote;
                    }
                })();
            }
            return this.waiter[instance.uid];
        },
        async populateRemoteUpdate(event) {
            if (this.handler[event.instance.uid] !== undefined) {
                // Http is pending right now
                this.remote[event.instance.uid] = event.instance.version;
            } else {
                // Else fire off update for instance, somebody just changed it
                await this.resolveNewVersion(event.instance);
            }
        },
        async populateRemoteDestroy(event) {
            io.change(true);
            let local = await store.dispatch("getInstanceByUid", event.instance.uid);
            if (local != undefined) {
                store.commit("deleteInstance", local);
            }
            io.change(false);
        },
        async resolveNewVersion(instance) {
            io.change(true);
            await store.dispatch("fetchInstance", instance);
            io.change(false);
        },
    },
});
