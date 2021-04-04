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
        async proposeUpdate(update, { type, id, uid }) {
            // Require Type, Id, Uid
            if (env.changesLocked) return;
            this.handler[uid] = Object.assign({}, this.handler[uid], update); // Merge updates
            if (!this.waiter[uid]) {
                // Already waiting to push update?
                this.waiter[uid] = (async () => {
                    await sleep(this.coolDown);
                    delete this.waiter[uid];
                    let newInstance = await api.update_partial(type, id, this.handler[uid]);
                    delete this.handler[uid];
                    if (this.remote[uid] !== undefined) {
                        // Ws finished before http - resolve miss match
                        if (this.remote[uid] !== newInstance.version) await this.resolveNewVersion(newInstance);
                        delete this.remote[newInstance.uid]; // Unset remote version
                    }
                    return newInstance;
                })();
            }
            return this.waiter[uid];
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
            let localInstance = await store.dispatch("getInstanceByUid", event.instance.uid);
            if (localInstance) {
                store.commit("deleteInstance", localInstance);
                if (localInstance.type == "wall") {
                    env.resolveWallDeleted(localInstance);
                }
            }
            io.change(false);
        },
        async resolveNewVersion(instance) {
            io.change(true);
            let localInstance = await store.dispatch("getInstanceByUid", instance.uid);
            await store.dispatch("fetchInstance", localInstance ? localInstance : instance);
            io.change(false);
        },
    },
});
